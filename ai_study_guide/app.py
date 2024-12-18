from flask import Flask, request, jsonify
from utils import generate_pdf
from nlp_models import summarize_video

app = Flask(__name__)

@app.route('/process_video', methods=['POST'])
def process_video():
    # Assuming 'video_transcript' is part of the request data
    data = request.get_json()
    transcript = data.get('video_transcript', '')  # Get video transcript from the request

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    # Generate the summary of the transcript
    summary = summarize_video(transcript)
    
    # Generate PDF (assuming you have this logic in utils.py)
    pdf_file = generate_pdf('quiz', summary)  # Example: passing summary instead of 'quiz'

    # Return response
    return jsonify({"summary": summary, "pdf_path": pdf_file}), 200

if __name__ == '__main__':
    app.run(debug=True)
