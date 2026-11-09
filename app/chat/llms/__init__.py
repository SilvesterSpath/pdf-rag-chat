from .chatopenai import build_llm
from functools import partial

llm_map = {
  "gpt-4o": partial(build_llm, model_name="gpt-4o"),
  "gpt-4o-mini": partial(build_llm, model_name="gpt-4o-mini"),
}

