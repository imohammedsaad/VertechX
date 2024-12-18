import spacy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

nlp = spacy.load("en_core_web_sm")

def generate_notes(text):
    doc = nlp(text)
    summary = " ".join([sent.text for sent in doc.sents][:5])  # Simple summarization (First 5 sentences)
    return summary.encode()

def generate_quiz(text):
    # Example: Create a quiz based on keywords
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha][:10]
    quiz = "\n".join([f"Define: {kw}" for kw in keywords])
    return quiz.encode()
