from flask import Flask, render_template, request, jsonify
import openai
import fitz  # PyMuPDF

app = Flask(__name__)


# Read the API key from a text file
def load_api_key():
    with open('config.txt', 'r') as file:
        return file.read().strip()

openai.api_key = load_api_key()

pdf_text = ""  # Global variable for storing extracted text

# Route for serving the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading and processing the PDF
@app.route('/query', methods=['POST'])
def query():
    global pdf_text
    file = request.files.get('file')
    user_query = request.form['query']

    # Process the PDF if a file is uploaded
    if file and file.filename.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()

    if not pdf_text:
        return jsonify({'response': 'Please upload a PDF first.'})

    # Use OpenAI to generate a response using gpt-3.5-turbo
    prompt = f"The following is text extracted from a PDF document:\n\n{pdf_text}\n\nUser Query: {user_query}\n\nBased on the document, please provide an answer."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return jsonify({'response': response['choices'][0]['message']['content'].strip()})

if __name__ == '__main__':
    app.run(debug=True,port=8090)

