from transformers import AutoModelForCausalLM, AutoTokenizer

# モデルとトークナイザーの準備
MODEL_NAME = "gpt2"  # Hugging Faceから利用するモデル名
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def generate_response(prompt: str, max_length: int = 100) -> str:
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
