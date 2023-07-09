import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import subprocess
from io import StringIO


app = FastAPI()


class CodeData(BaseModel):
    code: str
    code_type: str


@app.post("/execute", response_model=Dict[str, Any])
async def execute_code(code_data: CodeData):
    if code_data.code_type == "python":
        try:
            buffer = StringIO()
            sys.stdout = buffer
            exec(code_data.code)
            sys.stdout = sys.__stdout__
            exec_result = buffer.getvalue()

            return {"output": exec_result} if exec_result else {"message": "OK"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif code_data.code_type == "shell":
        try:
            output = subprocess.check_output(code_data.code, stderr=subprocess.STDOUT, shell=True, text=True)
            return {"output": output.strip()} if output.strip() else {"message": "OK"}
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=400, detail=str(e.output))

    else:
        raise HTTPException(status_code=400, detail="Invalid code_type")


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("remote:sandbox", host="localhost", port=80)