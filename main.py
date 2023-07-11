import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
from tools import PythonInterpreter


load_dotenv('token.env')
LLM_API_KEY = os.environ.get('LLM_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')




#build out the tools the AI will be able to use
llm = OpenAI(temperature=0, openai_api_key=LLM_API_KEY)
#check out alternatives on huggingface, not sure if using these require paid membership
# https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID, k=10)

def reflect_on_tool_options():
    llm.predict("AI: considering the previous human message, I don't have a tool that seems sufficient for the task given. I should explain my reasoning to the human.")


tools = [
    #tools to add: 
        # that reddit ML model that does webscraping intelligently
        # wolfram alpha
        # Apify, maybe replace search with something from here
        # pinecone search
        # pinecone index creation
        # wikipedia
        # pythonREPL
        # read files
        # image generation
    Tool(
        name="No Tool",
        func = reflect_on_tool_options,
        description="""
        Useful when none of the other tools available appear to be a good choice. 
        You should use this if you are asked to perform a task or answer a question and are unable to successfully complete the task or answer the question. 
        """
    ),
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
        Used to verify an answer determined after utilizing the "Search" tool. Take your Final Answer and phrase it as a question, based on the results determine if you are correct. 
        If not, try using the search tool again with this in mind. 
        For example, if asked "who was the US president in 1991?" and you determine the answer is "George H.W. Bush", you should use this tool with the input "was George H.W. Bush the US President in 1991?"
        """,
    ),
    PythonInterpreter(),
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
    input_variables=["chat_history", "input", "agent_scratchpad"],
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
    userinput = userinput.removeprefix('user input: ')
    agent_chain.run(input=userinput)





###### RLHF Mechanism ######

    # create a short term memory store of last user input and AI output, call it LastInteraction
    # each conversation should have a unique key, call it ConversationKey, and each LastInteraction should be given a integer value based on the order it occurs starting at 0, call it ConversationIndex
    # use a Tool that can classify sentiment of user input call it JudgeLastInteraction
    # based on JudgeLastInteraction the specific LastInteraction should be stored in a negative or positive index of a vector store
        # this should contain context details of conversation unique ConversationKey and ConversationIndex
    # memory retrieval tool would then be set up to query both positive and negative index for past conversations and apply positive or negative context of the respective Index results



