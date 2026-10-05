from langchain.chat_models import ChatOpenAI

def build_llm(chat_args):

  return ChatOpenAI(
    streaming=chat_args.streaming,
    model_name="gpt-3.5-turbo"
  )