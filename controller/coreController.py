from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class CoreController:
    def __init__(self):
        model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def conv(self, user_input, max_new_tokens=100):
        # Encode the user input and generate a response
        new_user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt').to(self.device)

        # If you want to maintain context, you'd concatenate previous chat history here
        chat_history_ids = new_user_input_ids

        with torch.no_grad():
            chat_history_ids = self.model.generate(
                chat_history_ids,
                max_length=chat_history_ids.shape[-1] + max_new_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2,
            )

        response = self.tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
