from openai import OpenAI

from zev.llms.inference_provider_base import InferenceProvider
from zev.llms.openai.provider import OpenAIProvider
from zev.config import config


class OllamaProvider(OpenAIProvider):
    """
    Same as OpenAIProvider, but takes a different base url and model.
    """

    def __init__(self):
        if not config.ollama_base_url:
            raise ValueError("OLLAMA_BASE_URL must be set. Try running `zev --setup`.")
        if not config.ollama_model:
            raise ValueError("OLLAMA_MODEL must be set. Try running `zev --setup`.")
        self.client = OpenAI(base_url=config.ollama_base_url)
        self.model = config.ollama_model
