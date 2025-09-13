import io, os
import requests
from pdf2image import convert_from_path

def convert_and_transcribe_pdf(pdf_path, api_key):

    full_transcription = []
    
    try:
        # Convert PDF pages to a list of Pillow Image objects in memory.
        # This is the crucial step to avoid saving files to disk.
        images = convert_from_path(pdf_path)
        print("Number of pages: ",len(images))
        for i, image in enumerate(images):
            # Create an in-memory byte buffer
            img_byte_arr = io.BytesIO()
            # Save the image into the buffer as a JPEG
            image.save(img_byte_arr, format='JPEG')
            # Reset the buffer's position to the beginning
            img_byte_arr.seek(0)
            
            # Prepare data for API request
            url = 'https://api.ocr.space/parse/image'
            files = {'file': (f'page_{i+1}.jpg', img_byte_arr.getvalue(), 'image/jpeg')}
            payload = {
                'apikey': api_key,
                'isOverlayRequired': False
            }
            
            # Send the request
            response = requests.post(url, files=files, data=payload)
            result = response.json()
            
            # Check for API errors
            if result['IsErroredOnProcessing']:
                error_message = result.get('ErrorMessage', 'Unknown API error')
                full_transcription.append(f"Page {i+1} Error: {error_message}")
            elif 'ParsedResults' in result:
                page_text = result['ParsedResults'][0]['ParsedText']
                full_transcription.append(page_text)
            print(f"[+]Page {i+1} completed")
    
    except Exception as e:
        return f"An error occurred: {e}"
    print("[+]All pages scanned")
    return "\n\n".join(full_transcription).strip()

def save_to_text_file(text_content, output_filename):
    """Saves the transcribed text to a .txt file."""
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"[+]Transcription saved to {output_filename}")
    except Exception as e:
        print(f"Failed to save file: {e}")


pdf_file_path = 'sample.pdf'
ocr_api_key = os.getenv('OCR_API')

# Get the full transcribed text
transcribed_text = convert_and_transcribe_pdf(pdf_file_path, ocr_api_key)


if not transcribed_text.startswith("An error occurred"):

    output_file_name = 'input_note.txt'
    save_to_text_file(transcribed_text, output_file_name)
else:
    print(transcribed_text)