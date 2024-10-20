import base64
import json
from PIL import Image
import io
import fireworks.client

fireworks.client.api_key = 'fw_3ZizSNVsSYhgFhtdGx2MME1M'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def preprocess_image(image_path):
    # For simplicity, we'll just open and convert to RGB
    with Image.open(image_path) as img:
        img = img.convert('RGB')
    
    # Save as JPEG in memory
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return base64.b64encode(img_byte_arr).decode('utf-8')

def classify_document(image_base64):
    response = fireworks.client.ChatCompletion.create(
        model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": "What type of document is this? Is it a passport or a driver's license? Please respond with just 'passport' or 'driver's license'.",
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                },
            }],
        }],
    )

    document_type = response.choices[0].message.content.strip().lower()

    return "passport" if "passport" in document_type else "driver's license" if "driver's license" in document_type else "unknown"

def extract_information(image_base64, document_type):
    prompt = f"""
    You are an AI assistant trained to analyze images of documents. 
    The image provided is a {document_type}. 
    Your task is to extract and report the following information from the image:
    - Full Name
    - Date of Birth
    - {'Passport' if document_type == 'passport' else 'License'} Number
    - Expiry Date

    Please format the response exactly as follows, with one field per line:
    Full Name: [extracted full name]
    Date of Birth: [extracted date of birth]
    {'Passport' if document_type == 'passport' else 'License'} Number: [extracted number]
    Expiry Date: [extracted expiry date]
    
    If a field is not visible or cannot be determined from the image, write 'Not visible' for that field.
    Remember, you are analyzing an image, not accessing real personal data.
    """
    
    response = fireworks.client.ChatCompletion.create(
        model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        messages=[{
            "role": "system",
            "content": "You are an AI assistant trained to extract information from images of documents. You should only report information visible in the provided image."
        }, {
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt,
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                },
            }],
        }],
        max_tokens=1000,
        temperature=0.2
    )

    extraction_result = response.choices[0].message.content

    # Parse the extracted information
    extracted_info = {
        "full_name": "Not visible",
        "date_of_birth": "Not visible",
        "document_number": "Not visible",
        "expiry_date": "Not visible",
    }
    
    current_field = None
    for line in extraction_result.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if "name" in key:
                current_field = "full_name"
            elif "birth" in key:
                current_field = "date_of_birth"
            elif "number" in key:
                current_field = "document_number"
            elif "expiry" in key or "expiration" in key:
                current_field = "expiry_date"
            if current_field:
                extracted_info[current_field] = value if value != "Not visible" else extracted_info[current_field]
    
    print("Extracted info:", extracted_info)
    return extracted_info

def validate_information(extracted_info):
    # Implement more robust validation logic here
    # For this PoC, we'll check if all fields are non-empty and have a minimum length
    return all(len(value) > 3 for value in extracted_info.values())

def generate_output(document_type, extracted_info, is_valid):
    return {
        "document_type": document_type,
        "extracted_information": extracted_info,
        "is_valid": is_valid
    }

def process_document(image_path):
    image_base64 = preprocess_image(image_path)
    document_type = classify_document(image_base64)
    extracted_info = extract_information(image_base64, document_type)
    is_valid = validate_information(extracted_info)
    return generate_output(document_type, extracted_info, is_valid)

if __name__ == "__main__":
    import os

    upload_folder = "upload"
    results = []

    for filename in os.listdir(upload_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(upload_folder, filename)
            result = process_document(image_path)
            results.append(result)

    for result in results:
        print(json.dumps(result, indent=2))
        print("-" * 50)  # Separator between results
