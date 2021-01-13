from transformers import pipeline

def summarize(text): 
    summarizer = pipeline('summarization')

    summary_text = summarizer(text)[0]['summary_text']
    return summary_text