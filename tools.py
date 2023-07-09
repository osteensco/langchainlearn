from langchain.tools.base import BaseTool
import requests
from ast import literal_eval





class SandboxTool(BaseTool):
    name = "SandboxTool"
    description = '''Useful for when you need to execute python code or install library by pip for python code. 
    The input to this tool should be a comma separated list of numbers of length two, 
    the first value is code_type(type:String), the second value is code(type:String) needed to execute. 
    For example: 
    ["python", "print(1+2)"], ["shell", "pip install langchain"], ["shell", "ls"] ... '''

    def _run(self, query: str) -> str:
        return self.remote_request(query)

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("PythonRemoteReplTool does not support async")

    def remote_request(self, query: str) -> str:
        list = literal_eval(query)
        url = "http://localhost:80/execute"
        headers = {
            "Content-Type": "application/json",  
        }
        json_data = {
            "code_type": list[0],
            "code": list[1]
        }
        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Request failed, status code：{response.status_code}"









