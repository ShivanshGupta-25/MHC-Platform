# from transformers import GPT2Tokenizer, GPT2LMHeadModel
# import torch

class CoreController:
    def __init__(self):
        # Load tokenizer and model
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-xl")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2-xl")
        self.model.eval()

        # Use CUDA if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def conv(self, user_input, max_length=150):
        # Prepend with a simple conversational context
        prompt = f"The following is a conversation with a compassionate mental health chatbot.\nUser: {user_input}\nChatbot:"

        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + max_length,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the chatbot's response
        if "Chatbot:" in response:
            response = response.split("Chatbot:")[-1].strip()
        return response