from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv


load_dotenv()

class StreamingHandler(BaseCallbackHandler):
  def on_llm_new_token(self, token: str, **kwargs) -> None:
    print(token)



chat = ChatOpenAI(
  streaming=True,
  callbacks=[StreamingHandler()]
  )

prompt = ChatPromptTemplate.from_messages([
  ("human", "{content}")
])

chain = LLMChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"tell me a joke"}):
  print(output)


""" messages = prompt.format_messages(content="Tell me a joke")

for message in chat.stream(messages):
  print(message.content) """

# output = chat.__call__(messages)
# output = chat.invoke(messages)

