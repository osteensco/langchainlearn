import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.memory import ConversationBufferMemory



load_dotenv('token.env')
LLM_API_KEY = os.environ.get('LLM_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')


search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID, k=10)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="""
        Useful for when you need to answer questions about current events. 
        When parsing results be sure to use the most common answer you find as that is most likely to be the correct answer.
        If you use this tool at all, after determining an answer use the "Verify Search" tool to verify your answer.
        """,
    ),
    Tool(
        name="Verify Search",
        func=search.run,
        description="""
        Used to verify an answer determined after utilizing the "Search" tool. 
        Take your Final Answer and phrase it as a question, based on the results determine if you are correct. If not try using the search tool again.
        """,
    )
]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
memory = ConversationBufferMemory(memory_key="chat_history")


llm = OpenAI(temperature=0, openai_api_key=LLM_API_KEY)


llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)


# agent_chain.run(input="Who is Tennessee's head football coach for the 2023 season?")
while True:
    userinput = input('user input: ')
    agent_chain.run(input=userinput)


