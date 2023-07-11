import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import subprocess
from io import StringIO






app = FastAPI()



class CodeData(BaseModel):
    req: str
    code: str



def display_output(raw_output):
    
    return_code = raw_output.returncode

    if return_code == 0:
        output = raw_output.stdout.decode()
    else:
        output = f'''There was an error: \n{raw_output.stderr.decode()}'''

    return output





@app.post("/python", response_model=Dict[str, Any])
async def execute_code(code_data: CodeData):
    try:
        with open('adhoc/requirements.txt', 'w') as req:
            req.write(code_data.req)
        with open('adhoc/scratchpad.py', 'w') as code:
            code.write(code_data.code)
        
        outputs = {}
        req_exec_result = subprocess.run(['pip', 'install', '-r', 'adhoc/requirements.txt'], capture_output=True)
        outputs['requirements.txt'] = display_output(req_exec_result)
        
        python_exec_output = subprocess.run(['python', '-u', 'adhoc/scratchpad.py'], check=False, capture_output=True)
        outputs['scratchpad.py'] = display_output(python_exec_output)
 
        print(outputs)
        return {"output": outputs} if outputs else {"message": "OK"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
    


    
    # elif code_data.code_type == "shell":
    #     try:
    #         output = subprocess.check_output(code_data.code, stderr=subprocess.STDOUT, shell=True, text=True)
    #         return {"output": output.strip()} if output.strip() else {"message": "OK"}
    #     except subprocess.CalledProcessError as e:
    #         raise HTTPException(status_code=400, detail=str(e.output))

    # else:
    #     raise HTTPException(status_code=400, detail="Invalid code_type")






