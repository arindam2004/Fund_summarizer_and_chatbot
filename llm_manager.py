##'''Handles model selection and abstraction, 
##to easily swap Llama 3.2, GPT-4o mini, DeepSeek R1, etc.'''

import os
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self, model_name="llama-3.2"):
        self.model_name = model_name
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY"),
        }

    def generate(self, prompt, **kwargs):
        if self.model_name == "llama-3.2":
            return self._call_llama(prompt, **kwargs)
        elif self.model_name == "gpt-4o-mini":
            return self._call_openai(prompt, **kwargs)
        elif self.model_name == "deepseek-chat":
            return self._call_deepseek(prompt, **kwargs)
        else:
            raise ValueError("Unsupported model")

    def _call_llama(self, prompt, **kwargs):
        import requests
        import json
        url = "http://localhost:11434/api/generate"  # or your local endpoint
        data = {
            "model": "llama3.2",
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
        }
        response = requests.post(url, json=data)
        # Handle streaming JSON lines
        output = ""
        for line in response.text.strip().splitlines():
            try:
                obj = json.loads(line)
                # Some lines may have 'response', some may not
                if "response" in obj:
                    output += obj["response"]
            except Exception:
                continue  # skip lines that are not valid JSON
        return output.strip()

    def _call_openai(self, prompt, **kwargs):
        from openai import OpenAI
        client = OpenAI(api_key=self.api_keys["openai"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7),
        )
        return response.choices[0].message.content


    def _call_deepseek(self, prompt, **kwargs):
        import requests

        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_keys['deepseek']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",  # or "deepseek-ai/DeepSeek-R1"
            "messages": [
                {"role": "system", "content": "You are a helpful finanacial analyst."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
            "stream": False
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"DeepSeek API error: {response.status_code} {response.text}")
