from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLMService:
    def __init__(self):
        # Using BLOOM-560m - a smaller, efficient open-source LLM
        self.model_name = "bigscience/bloom-560m"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
    async def generate_text(self, prompt: str, max_length: int = 500) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            temperature=0.7,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)