import os
import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()


class LocalEmbedding:
    def __init__(self) -> None:
        pass

    @staticmethod
    def set(model_name: str = "text-embedding-ada-002"):
        if model_name != "text-embedding-ada-002":
            return HuggingFaceEmbedding(
                model=AutoModel.from_pretrained(model_name, torch_dtype=torch.float16),
                tokenizer=AutoTokenizer.from_pretrained(model_name, torch_dtype=torch.float16),
                cache_folder=os.path.join(os.getcwd(), "data/huggingface"),
                trust_remote_code=True
            )
        else:
            return OpenAIEmbedding()