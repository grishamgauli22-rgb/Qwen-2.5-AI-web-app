import os
import subprocess

# Set Hugging Face cache folder on the F: drive
os.environ["HF_HOME"] = r"F:\Users\grish\Projects\Programming\Python\GPT2\.cache"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")

# Give the AI strict instructions on how to format commands
system_prompt = (
    "You are a helpful chat assistant. "
    "Respond using normal conversational plain text. "
    "DO NOT use code blocks or bash commands unless the user explicitly asks to run a system command or execute a script."
)

messages = [{"role": "system", "content": system_prompt}]

print("\n==========================================")
print("     Qwen 2.5 CLI Command Agent     ")
print("==========================================\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        break
    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})
    
    # Generate response
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(**model_inputs, max_new_tokens=200, do_sample=True, temperature=0.7)
    
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print(f"\nAI:\n{response}\n")
    messages.append({"role": "assistant", "content": response})

    # Simple check to see if the AI suggested a bash command block
    if "```bash" in response:
        try:
            # Extract the command between ```bash and ```
            start = response.find("```bash") + len("```bash")
            end = response.find("```", start)
            command = response[start:end].strip()

            if command:
                confirm = input(f"⚠️  AI wants to run this command: [ {command} ]\nRun it? (y/n): ")
                if confirm.strip().lower() == 'y':
                    print("Running command...")
                    # Execute the command in PowerShell/CMD
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    output = result.stdout if result.returncode == 0 else result.stderr
                    print(f"Output:\n{output}")
                    
                    # Feed the output back to the AI so it knows what happened!
                    messages.append({"role": "user", "content": f"Command output:\n{output}"})
                else:
                    print("Command cancelled.")
        except Exception as e:
            print(f"Error executing command: {e}")