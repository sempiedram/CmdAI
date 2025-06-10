
import google.generativeai as genai
import typing_extensions as typing
import json
import sys
import os

gemini_key = os.getenv("GEMINI_API_PRIVATE_KEY")
if not gemini_key:
	print("GEMINI_API_PRIVATE_KEY environment variable not set")
	exit()

if len(sys.argv) < 3:
	exit()

original_folder = sys.argv[1]
task = " ".join(sys.argv[2:])

genai.configure(api_key=gemini_key, transport='rest')
model = genai.GenerativeModel("gemini-2.5-pro-preview-05-06")
# model = genai.GenerativeModel("gemini-2.0-flash-exp")
prompt = """
The user will give you a description of a Python script they want you to write.
The operating system is Windows.
You can't install new Python libraries.
The script you generate will be written into a script.py file and executed.
You will be provided a function called tai(prompt) that generates a string with AI based on the given prompt.
DO NOT DEFINE OR WRITE THE tai function, simply write the function call.
DO NOT WRITE A tai STUB, do not include a placeholder.
When the user includes a reference to tai, like "use tai for name of a random USA president" you should include the tai call in your generated script to generate text where required.
Use tai even when the user doesn't explicitly says so, when it makes sense.
You can USE tai to test if a file name fits a description the user gave. For example tai("Is <file name> about physics? Answer only y or n").
You don't need to use tai for things you can easily check with Python, such as if a file is a png, or if a path is a directory.
Add comments to the script to explain what each part of the script does.
In the generated script add prints to show the steps of the script as they happen.
Sometimes the user will use placeholders. There is no specific syntax for placeholders, but examples are: <original file>, (file name here), -current date- or similar.
When the user uses placeholders you should pass the information the user referenced there, instead of leaving the placeholder as is.
ONLY OUTPUT THE SCRIPT, DO NOT EXECUTE IT, NOR ADD A LINE WITH THE NAME OF THE SCRIPT
DO NOT ADD A CODE BLOCK, ONLY THE CONTENTS OF THE SCRIPT FILE

This is what the user needs the script to do: {}
Now generate the script.""".format(task)
# print("prompt: '{}'".format(prompt))

class CommandJson(typing.TypedDict):
	cmd: str

response = model.generate_content(
		prompt,
		generation_config=genai.types.GenerationConfig(
			response_mime_type="application/json",
			response_schema=CommandJson,
			stop_sequences=["@!;S"],
			max_output_tokens=100000
		)
	)

response_text = response.text
try:
	filename = os.path.join(original_folder, "cai_response.txt")
	with open(filename, "w") as output_file:
		output_file.write(response_text)
except IOError:
	print("Failed writing received response to cai_response.txt")

generated_cmd = json.loads(response_text)["cmd"]
print("{}".format(generated_cmd))

tai_contents = ""
if "tai(" in generated_cmd:
	# Include the contents of tai_include.py
	with open("tai_include.py", "r") as tai_file:
		tai_contents = tai_file.read()

try:
	filename = os.path.join(original_folder, "cai_script.py")
	with open(filename, "w") as output_file:
		output_file.write(tai_contents + "\n# Generated script starts here.\n" + generated_cmd)
except IOError:
	print("Couldn't write to script.bat")

