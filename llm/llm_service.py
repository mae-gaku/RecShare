# llm_service.py

from llama_index.llms.llama_cpp import LlamaCPP

from langchain_community.llms import LlamaCpp


# LLMのセットアップ
model_path = "./llm/SmolLM2-360M-Instruct-Q5_K_M.gguf"

llm = LlamaCpp(
    model_path=model_path,
    n_ctx=2048,
    temperature=0.75,
    max_tokens=2000,
    top_p=1,
    verbose=True,  # Verbose is required to pass to the callback manager
)


# LLMを返す関数
def get_llm():
    return llm