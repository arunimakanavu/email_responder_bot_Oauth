from transformers import pipeline

def generate_response(prompt):
    generator = pipeline("text-generation", model="gpt2")
    response = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return response
