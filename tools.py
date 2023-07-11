from langchain.tools.base import BaseTool
import requests
from ast import literal_eval



class PythonInterpreter(BaseTool):
    name = "Python Interpreter"
    description = '''Useful for when you need to execute python code or install library by pip for python code. 
    The input to this tool should be a  list of two strings, 
    the first value is req(type:String), the second value is code(type:String) needed to execute. 
    These strings will be used to create a requirements.txt and scratchpad.py file respectively. 
    The strings should include any line breaks so that code and requirements.txt would be properly formatted and ready for execution.
    You must be sure to include any libraries in the first string that you would need to import in your python script, the second string.
    The requirements and code you provide this tool will be used to create the requirements.txt file and python file. The python file will then be executed for you.
    The output you receive should tell you of any errors. If there any errors you are not done yet. 
    Be sure to attempt to write your code again based on this feedback. Continue this process until the code produces no errors.
    Examples: 
    ["math", "import math\\n\\nprint(math.pi)"], 
    ["requests", "import requests\\n\\n# Making a GET request\\nr = requests.get('https://www.scottosteen.com')"], 
    '''
    # ["pandas", """import pandas as pd\\n\\nd = {'col1': [1, 2], 'col2': [3, 4]}\\ndf = pd.DataFrame(data=d)\\ndef print_columns(df):\\n    for col in df.columns:    print(f'\\n{col}\\n')\\n\\nprint_columns(df)"""] ... 
    # '''

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





