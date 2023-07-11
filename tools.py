from langchain.tools.base import BaseTool
import requests
from ast import literal_eval



class PythonInterpreter(BaseTool):
    name = "Python Interpreter"
    description = '''Useful for when you need to execute python code. 
    This tool sends an API post request to a docker container that has an environment set up to run the code you give it via post request.
    The endpoint will receive the data you provide it and will create a requirements.txt file and a scratchpad.py file. 
    It will then run the command pip install -r requirements.txt and afterwards execute the scratchpad.py script. Any output this script produces in the terminal will be returned to you in the response.
    If successful, the response will be structure like {'output': {'requirements.txt': 'Requirement already satisfied: requests...', 'scratchpad.py': 'hello world'}}.
    The input to this tool should be a list of two strings, the first value is req(type:String), the second value is code(type:String). Both are needed to execute the tool properly. 
    These strings will be used to create a requirements.txt and scratchpad.py file respectively. 
    The strings should include any line breaks so that code and requirements.txt would be properly formatted and ready for execution.
    You must be sure to include any libraries in the first string that you would need to import in your python script, the second string.
    The requirements and code you provide this tool will be used to create the requirements.txt file and python file. The python file will then be executed for you.
    The output you receive should tell you of any errors. If there any errors you are not done yet. 
    Be sure to attempt to write your code again and make changes based on any errors you receive. Continue this process until the code produces no errors.
    If you receive an empty string for 'scratchpad.py' then you probably need to check your code and make sure you are printing any pertinent information to the console.
    Examples: 
    ["", "import math\\n\\nprint(math.pi)"], 
    ["requests", "import requests\\n\\n# Making a GET request\\nr = requests.get('https://www.scottosteen.com')"], 
    ["requests\\nbeautifulsoup4", "import requests\\nfrom bs4 import BeautifulSoup\\n\\nr = requests.get('https://www.scottosteen.com/')\\n\\nsoup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')\\n\\nfirst_sentence = soup.find('p').get_text(strip=True)"]
    '''


    def _run(self, query: str) -> str:
        return self.remote_request(query)

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("PythonInterpreter does not support async")

    def remote_request(self, query: str) -> str:
        list = literal_eval(query)
        url = "http://localhost:80/python"
        headers = {
            "Content-Type": "application/json",  
        }
        json_data = {
            "req": list[0],
            "code": list[1]
        }
        
        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Request failed, status code：{response.status_code}"






