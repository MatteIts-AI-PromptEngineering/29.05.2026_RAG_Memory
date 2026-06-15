import logging

from ollama import Client as OllamaClient

logger = logging.getLogger(__name__)


class Client:
    def __init__(
            self,
            model: str,
            api_url: str,
            temperature: float,
            top_p: float,
            num_predict: int,
            system_prompt: str,
            window_size: int
    ):
        self._client = OllamaClient(api_url)
        self.model = model
        self.system_prompt = system_prompt
        self.window_size = window_size
        self._options = {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": num_predict,
        }
        logger.info(
            f"Client pronto | model={model} | url={api_url} | "
            f"temp={temperature} | top_p={top_p} | num_predict={num_predict} | window={window_size}"
        )

    def complete(self, user_prompt: str, history: list) -> str:
        messages = self._build_messages(user_prompt, history)
        
        response = self._client.chat(
            model=self.model,
            messages=messages,
            options=self._options
        )
        answer = response["message"]["content"]
        
        return answer

    def _build_messages(self, user_prompt: str, history: list) -> list:
        system = {"role": "system", "content": self.system_prompt}
        recent = history[-self.window_size:]

        past = []
        for turn in recent:
            if isinstance(turn, dict):
                past.append({"role": turn.get("role", "user"), "content": self._to_str(turn.get("content", ""))})
            else:
                past.append({"role": "user",      "content": self._to_str(turn[0])})
                past.append({"role": "assistant",  "content": self._to_str(turn[1])})

        return [system] + past + [{"role": "user", "content": user_prompt}]

    @staticmethod
    def _to_str(content) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return " ".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            ).strip()
        return str(content)
