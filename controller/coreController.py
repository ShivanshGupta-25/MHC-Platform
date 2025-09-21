from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class CoreController:
    def __init__(self):
        # model_name = "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        model_name = "gpt2"
        # Disable fast tokenizer to avoid conversion errors
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.model.eval()

    def conv(self, user_input, max_new_tokens=200):
        system_prompt = "You are a compassionate, supportive mental health assistant. Provide thoughtful and safe responses to help the user."
        prompt = f"<s>[INST] {system_prompt}\nUser: {user_input} [/INST]"

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "[/INST]" in response:
            response = response.split("[/INST]")[-1].strip()
        return response
