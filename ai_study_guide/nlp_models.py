from transformers import pipeline, BartTokenizer, BartForConditionalGeneration

# Initialize the summarizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def split_into_chunks(text, max_length=1024):
    """
    Split a long transcript into smaller chunks of max_length tokens.
    """
    tokens = text.split()
    chunks = []
    while len(tokens) > max_length:
        chunk = ' '.join(tokens[:max_length])
        chunks.append(chunk)
        tokens = tokens[max_length:]
    if tokens:
        chunks.append(' '.join(tokens))
    return chunks

def summarize_video(transcript):
    """
    Summarize a video transcript. If the transcript is too long, split it into chunks.
    """
    # Split transcript into chunks if necessary
    chunks = split_into_chunks(transcript, max_length=1024)

    # Summarize each chunk and combine the results
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine all summaries into a final summary
    full_summary = ' '.join(summaries)
    return full_summary
