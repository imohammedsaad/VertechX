from transformers import pipeline, BartTokenizer, BartForConditionalGeneration

# Initialize the summarizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

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
