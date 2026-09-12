from fastapi import FastAPI, Form
import subprocess
from pydantic import BaseModel

class RunRequest(BaseModel):
    input: str = ""

app = FastAPI()



@app.get("/")
def hello():
    return {"msg": "hello"}

@app.post("/send-code")
def write(code: str = Form(...)):
    with open("hello.py", "w") as file:
        file.write(code)

    return {"message": "Code received"}


@app.post("/run")
def run(request: RunRequest):

    subprocess.run([
        "docker", "build",
        "-t", "my-python-app",
        "."
    ])

    result = subprocess.run(
        ["docker", "run", "--rm", "-i", "my-python-app"],
        input=request.input,
        capture_output=True,
        text=True
    )

    return {
        "output": result.stdout,
        "error": result.stderr
    }