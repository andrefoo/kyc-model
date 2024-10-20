# Document Information Extraction

This repository contains a Python script for extracting information from passport and driver's license images using the Fireworks AI API.

## Repository

This project is hosted on GitHub: [https://github.com/andrefoo/kyc-model.git](https://github.com/andrefoo/kyc-model.git)

## Setup

1. **Create a Fireworks AI account**
   - Sign up for a Fireworks AI account at [https://fireworks.ai/login](https://fireworks.ai/login)
   - Retrieve your API key from the User page

2. **Set up the API key**
   - Open the `document_extraction.py` file
   - Replace the placeholder API key on line 7 with your actual Fireworks AI API key:
     ```python:document_extraction.py
     fireworks.client.api_key = 'YOUR_API_KEY_HERE'
     ```

3. **Install required libraries**
   - Make sure you have Python installed on your system
   - Install the required libraries by running:
     ```
     pip install -r requirements.txt
     ```

## Usage

1. **Prepare your images**
   - Create an `upload` folder in the root directory of the project if it doesn't exist
   - Place your passport or driver's license images in the `upload` folder

2. **Run the script**
   - Open a terminal or command prompt
   - Navigate to the project directory
   - Run the script with:
     ```
     python document_extraction.py
     ```

3. **View results**
   - The script will process the image(s) in the `upload` folder
   - Results will be printed in the console as JSON output

## Features

- Automatic document type classification (passport or driver's license)
- Information extraction including full name, date of birth, document number, and expiry date
- Basic validation of extracted information

## Note

This project is for demonstration purposes only. Ensure you have the right to process any personal documents and comply with relevant data protection regulations.

