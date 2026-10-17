from transformers import pipeline

model_id = "Qwen/Qwen3-0.6B" ## Generative chat model


print("Loading model...")
generator = pipeline("text-generation", model=model_id)
print("Model loaded.")

messages = [
    {"role": "user", "content": "Explain what an EGFR mutation is in two sentences?"}
]

output = generator(messages, max_new_tokens=100, do_sample=False)

print("Generated response:")
print(output[0]['generated_text'][-1]["content"])

