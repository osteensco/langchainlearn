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




#build out the tools the AI will be able to use
llm = OpenAI(temperature=0, openai_api_key=LLM_API_KEY)
#check out alternatives on huggingface, not sure if using these require paid membership
# https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID, k=10)

tools = [
    #tools to add: 
        # that reddit ML model that does webscraping intelligently
        # wolfram alpha
        # Apify, maybe replace search with something from here
        # pinecone search
        # pinecone index creation
        # wikipedia
        # pythonREPL
        # image generation
    Tool(
        name="Predict",
        func = llm.predict,
        description="""
        Useful when a search is unnecessary. 
        If it is likely that the answer would not have changed since 2021 (it's currently 2023), then this tool should take priority over using the "Search" tool.
        """
    ),
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



#promt template
######## How to addSystem Promt???
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



#persistence 
memory = ConversationBufferMemory(memory_key="chat_history")#short term
### switch over to pinecone index


#define the AI
llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)


# agent_chain.run(input="Who is Tennessee's head football coach for the 2023 season?")
while True:
    userinput = input('user input: ')
    agent_chain.run(input=userinput)


