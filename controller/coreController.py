from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from textblob import TextBlob
import transformers

# Optional: suppress verbosity warnings from transformers
transformers.logging.set_verbosity_error()

class CoreController:
    def __init__(self, model_type="nous", model_name=None):
        """
        Initialize the model based on the chosen type.
        """
        self.model_type = model_type
        self.model_name = model_name

        if model_type == "gpt2":
            self.model_name = model_name or "gpt2"
        elif model_type == "nous":
            self.model_name = model_name or "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        elif model_type == "phi1.5":
            self.model_name = model_name or "microsoft/phi-1.5"
        elif model_type == "qwen2.5":
            self.model_name = model_name or "Qwen/Qwen2-0.5B"
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

        self._load_model()
        self.sentiment_analysis = pipeline("sentiment-analysis")

    def _load_model(self):
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            self.model.eval()
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
        except Exception as e:
            raise RuntimeError(f"Error loading model {self.model_name}: {str(e)}")

    def _generate_empathy_prompt(self, user_input):
        empathy_phrases = [
            "I'm so sorry you're feeling this way.",
            "It's completely okay to feel how you are feeling right now.",
            "I'm here to listen and help you through this.",
            "You're not alone in this, and it's great you're reaching out."
        ]

        sentiment = self.sentiment_analysis(user_input)[0]['label']
        if sentiment == 'NEGATIVE':
            empathy_prompt = f"{empathy_phrases[0]} I understand that things might be tough right now. Let me know how I can help."
        elif sentiment == 'POSITIVE':
            empathy_prompt = f"{empathy_phrases[3]} It sounds like you're feeling good, but I'm here for you if you need anything."
        else:
            empathy_prompt = f"{empathy_phrases[1]} I'm here to support you in any way I can."

        return empathy_prompt
    
    def conv(self, user_input, max_new_tokens=150):
        # Use sentiment to guide model tone — not to hardcode response
        sentiment = self.sentiment_analysis(user_input)[0]['label']

        # Updated system prompt without "Suggested empathy:"
        system_prompt = (
            "You are a compassionate and supportive mental health assistant. "
            "You listen carefully, respond with empathy, and provide helpful guidance. "
            "You are not a doctor and do not give medical advice, but you offer emotional support and encouragement. "
            "Always respond in a calm, caring, and non-judgmental way."
        )

        # Let the model generate based on the user's message
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        print("Formatted prompt:\n", prompt)

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)

            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids=input_ids,
                    max_new_tokens=max_new_tokens,
                    pad_token_id=self.tokenizer.eos_token_id or self.tokenizer.pad_token_id,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.95,
                    repetition_penalty=1.1,
                )

            response = self.tokenizer.decode(output_ids[0][input_ids.shape[-1]:], skip_special_tokens=True)
            print("Generated response:", response)

            return response.strip()

        except Exception as e:
            print(f"Error during response generation: {str(e)}")
            return "I'm sorry, I wasn't able to generate a response. Could you try again later."
