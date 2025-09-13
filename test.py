from google import genai
import os
from dotenv import load_dotenv

load_dotenv() 
def main():
	client = genai.Client(api_key=os.getenv('GEMINI_API'))


	customPrompt = ""
	with open("custPrompt.txt","r") as f:
		customPrompt = f.read()

	input = ""
	with open("input_note.txt","r") as f:
		input = f.read()

	prompt = customPrompt+"\n \"" + input + "\n \""

	response = client.models.generate_content(
		#model = "gemma-3-1b-it",
		model="gemini-2.5-flash-lite",
		contents = prompt

	)

	res = response.text

	with open("response.txt", "w") as f:
		f.write(res)
	return "test.py run successfully"