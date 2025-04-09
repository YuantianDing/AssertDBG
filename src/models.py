
from langchain.chat_models import init_chat_model

MODELS = {
    "task": init_chat_model("o3-mini", model_provider="openai"),
    "assert": init_chat_model("o3-mini", model_provider="openai"),
    "split": init_chat_model("o1", model_provider="openai"),
}