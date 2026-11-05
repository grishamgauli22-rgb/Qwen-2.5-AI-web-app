import os

# Ensure model uses F: drive cache
os.environ["HF_HOME"] = r"F:\Users\grish\Projects\Programming\Python\GPT2\.cache"

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

# Global variables for model and tokenizer (loaded lazily)
tokenizer = None
model = None

def load_model_if_needed():
    global tokenizer, model
    if model is None:
        print("⏳ Loading local Qwen model into memory...")
        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")
        print("✅ Model loaded successfully!")

class ChatRequest(BaseModel):
    messages: list[dict]

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Load the model on the fly if it hasn't been loaded yet
    load_model_if_needed()

    # Apply Qwen chat template
    text = tokenizer.apply_chat_template(
        request.messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Generate response
    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs, max_new_tokens=250, do_sample=True, temperature=0.7
        )

    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response_text = tokenizer.batch_decode(
        generated_ids, skip_special_tokens=True
    )[0]

    return {"response": response_text}