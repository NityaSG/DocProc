from flask import Flask, request, jsonify
import requests
import os
import fitz 

app = Flask(__name__)

@app.route('/parse_pdf', methods=['POST'])
def parse_pdf():
    def extract_text_from_pdf(pdf_url):
        response = requests.get(pdf_url)
        response.raise_for_status() 

        with open('temp.pdf', 'wb') as file:
            file.write(response.content)

        text = ''
        with fitz.open('temp.pdf') as pdf_document:
            num_pages = pdf_document.page_count
            for page_num in range(num_pages):
                page = pdf_document.load_page(page_num)
                text += page.get_text()

        os.remove('temp.pdf')

        return text

    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid JSON format. Expecting a list of dictionaries.'}), 400

    if len(data) == 0 or 'pdf_url' not in data[0]:
        return jsonify({'error': 'PDF URL not provided in the request'}), 400

    pdf_url = data[0]['pdf_url']

    try:
        text = extract_text_from_pdf(pdf_url)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
