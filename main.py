import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate, LLMChain




load_dotenv('token.env')
APIKEY = os.environ.get('KEY')




question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

repo_id = "google/flan-t5-base"

llm = HuggingFaceHub(repo_id='openchat/openchat_8192', model_kwargs={"temperature": 0.1, "max_length": 64}, huggingfacehub_api_token=APIKEY)
print('connected')
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(question))







