
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

----- instructions -----

# What you will do

The user will give you a description of a Python script they want you to write.
Output only the contents of the short Python script that does what the request asks for.
The operating system is Windows 10.
The text you generate will be directly written to a file with .py extension.


# The tai(prompt) function

You will be provided a Python function called tai(prompt).
This tai() function outputs a textual response to the given prompt, using AI.
DO NOT DEFINE OR WRITE THE tai function, you can simply use the function call.
DO NOT WRITE A tai function STUB, do not include a placeholder.
When the user includes a reference to the tai function (for example: "use tai for name of a random USA president") you should include the tai function call in your generated script to generate text where required.
When it makes sense, and even if the user didn't explicitly request it, you can use the tai function, but only when it makes sense.
You can USE the tai function to test if a file name fits a description the user gave. For example tai("Is <file name> about physics? Answer only y or n"), and you could make decisions based on the tai function's response.
You don't need to use tai for things you can easily check with Python, such as if a file is a png, or if a path is a directory, or if a file name includes a string (use regex, for example), or to access metadata of a file.

# About libraries

If you really cannot do something with the default Python libraries, and you NEED some library,
you can add the import, and use it.

# Other gotchas

Add comments to the script to explain what each part of the script does.
In the generated script add print() calls to show the steps and progress of the script as it runs.
Sometimes the user will use placeholders. There is no specific syntax for placeholders, but examples are: <original file>, (file name here), -current date- or similar.
When the user uses placeholders you should pass the information the user referenced there, instead of using the placeholder as is written.
For example, if the user says "rename the files to <filename>.old.<extension>" you need to swap the placeholder for the file name and extension as required.

# IMPORTANT

ONLY OUTPUT THE SCRIPT, DO NOT EXECUTE IT, NOR ADD A LINE WITH THE NAME OF THE SCRIPT
DO NOT ADD A CODE BLOCK, ONLY THE CONTENTS OF THE SCRIPT FILE

----- end of instructions -----

This is what the user needs the script to do:

START OF REQUEST
{}
END OF REQUEST

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

