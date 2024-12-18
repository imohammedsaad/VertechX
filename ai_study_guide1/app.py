from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from utils.ai_tools import generate_notes, generate_quiz  # Import functions from ai_tools
from utils.pdf_processing import process_pdf  # Import process_pdf from utils folder
from utils.yt_processing import process_youtube_link  # Import YouTube link processor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded PDFs
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'mp4'}  # Allow pdf and video files

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to generate a new PDF
def generate_pdf(content, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, content)  # Simple example of adding content to PDF
    c.save()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_pdf', methods=['POST'])
def process_pdf_route():
    if 'pdf_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['pdf_file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the PDF (extract content)
        extracted_text = process_pdf(file_path)

        # Generate the processed PDF with extracted content
        extracted_notes = generate_notes(extracted_text).decode()
        processed_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        generate_pdf(extracted_notes, processed_pdf_path)

        # Return the generated PDF for download
        return send_file(processed_pdf_path, as_attachment=True, download_name="processed_file.pdf")

    return 'Invalid file format'

@app.route('/process_youtube', methods=['POST'])
def process_youtube_route():
    youtube_url = request.form.get('youtube_link')
    if not youtube_url:
        return 'No YouTube link provided.'
    
    # Process the YouTube link
    transcribed_text = process_youtube_link(youtube_url)
    
    # Generate notes and quiz from the transcribed content
    notes = generate_notes(transcribed_text).decode()
    quiz = generate_quiz(transcribed_text).decode()

    # Generate the processed PDF with notes and quiz
    processed_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_youtube_content.pdf')
    content = f"Notes:\n{notes}\n\nQuiz:\n{quiz}"
    generate_pdf(content, processed_pdf_path)

    # Return the generated PDF for download
    return send_file(processed_pdf_path, as_attachment=True, download_name="youtube_processed_file.pdf")

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
