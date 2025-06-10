
import google.generativeai as genai
import typing_extensions as typing
import json
import os

gemini_key = os.getenv("GEMINI_API_PRIVATE_KEY")
if not gemini_key:
	print("GEMINI_API_PRIVATE_KEY environment variable not set")
	exit()

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-pro")

class ResponseJson(typing.TypedDict):
	response: str

def tai(task):
	prompt = """
The user will give you a prompt, and you should respond with a short answer to the prompt.
Don't include anything extra, just the answer.
Valid response examples:
Prompt -> Response
"USA president" -> "Barack Obama"
"usa president" -> "Donald Trump" (or the name of some other USA president)
"What year did we reach the moon?" -> "1969"
"Format date 'december 10, 2023' to dd/mm/yy" -> "10/12/23"
If the prompt requires the answer to be long, it's fine, as long as it's JUST the answer.
The user's prompt is: {}
""".format(task)
	response = model.generate_content(
			prompt,
			generation_config=genai.types.GenerationConfig(
				response_mime_type="application/json",
				response_schema=ResponseJson,
				stop_sequences=["@!;S"],
				temperature=1.1,
				max_output_tokens=10000
			)
		)
	
	generated_response = json.loads(response.text)["response"]

	print("tai(\"{}\") -> \"{}\"".format(task, generated_response))

	return generated_response
