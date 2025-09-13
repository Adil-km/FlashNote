import io, os
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv() 

def ocr_image(image_path, api_key): 
    try:
        image = Image.open(image_path)

        if image.mode in ("P", "RGBA", "L"):
            image = image.convert("RGB")
            
        # Put image into a memory buffer
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)
        
        # Prepare data for API request
        url = 'https://api.ocr.space/parse/image'

        files = {'file': (os.path.basename(image_path), img_byte_arr.getvalue(), 'image/jpeg')}
        payload = {
            'apikey': api_key,
            'isOverlayRequired': False
        }
        
        # Send the request
        response = requests.post(url, files=files, data=payload)
        try:
            result = response.json()
        except Exception:
            return f"OCR API did not return JSON. Raw response: {response.text}"
        
        # Check for API errors
        if isinstance(result, dict):
            if result.get('IsErroredOnProcessing'):
                return f"Error: {result.get('ErrorMessage', 'Unknown API error')}"
            elif 'ParsedResults' in result:
                return result['ParsedResults'][0]['ParsedText'].strip()
            else:
                return "No text found."
        else:
            return f"Unexpected response format: {result}"


    except Exception as e:
        return f"An error occurred: {e}"

def save_to_text_file(text_content, output_filename):
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"[+] OCR result saved to {output_filename}")
    except Exception as e:
        print(f"Failed to save file: {e}")



def image_OCR(image_path):
    ocr_api_key = os.getenv('OCR_API')
    # Get the transcribed text
    text_result = ocr_image(image_path, ocr_api_key)

    if not text_result.startswith("An error occurred"):
        output_file_name = 'input_note.txt'
        save_to_text_file(text_result, output_file_name)
    else:
        print(text_result)
    