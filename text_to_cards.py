from google import genai
import os
from dotenv import load_dotenv

load_dotenv() 
def text_to_card():
	client = genai.Client(api_key=os.getenv('GEMINI_API'))


	customPrompt = ""
	with open("custPrompt.txt","r") as f:
		customPrompt = f.read()

	with open("input_note.txt", "r") as f:
		lines = f.readlines()

	# Keep only non-empty lines (stripping whitespace)
	lines = [line for line in lines if line.strip() != ""]

	with open("input_note.txt", "w") as f:
		f.writelines(lines)

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
	with open("input_note.txt","w") as f:
		f.write("")
	return "test.py run successfully"