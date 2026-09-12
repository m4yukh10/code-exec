# code-exec

A code execution system that runs Python code in isolated Docker containers, similar to an online compiler.

## Overview

`code-exec` takes Python code, packages it into a Docker image, runs that image as a temporary container, and returns the program's output.

The basic execution flow is:

```text
Python code
    ↓
program.py
    ↓
Docker image
    ↓
Temporary container
    ↓
Python execution
    ↓
stdout / stderr
    ↓
Container removed
```

Each execution happens inside a Docker container rather than directly on the host machine.

## How It Works

### 1. Write the code

The submitted Python code is written to:

```text
program.py
```

The file becomes part of the Docker build context.

### 2. Build the image

A Docker image is created from the project Dockerfile:

```bash
docker build -t my-python-app .
```

The image contains:

* Python
* the Docker working environment
* the submitted `program.py`

### 3. Run the program

The image is started as a temporary container:

```bash
docker run --rm -i my-python-app
```

The `--rm` flag automatically removes the container after execution finishes.

The Docker image itself remains available for subsequent runs.

### 4. Handle input

Programs that use Python's `input()` can receive input through standard input.

For example:

```python
name = input()
age = int(input())

print(f"{name} is {age}")
```

The execution request can provide:

```json
{
  "input": "Mayukh\n21\n"
}
```

The input is passed to the container through stdin.

The execution system treats input as text. Python itself determines how that input is interpreted:

```python
name = input()
```

keeps it as a string, while:

```python
age = int(input())
```

converts it to an integer.

### 5. Capture the result

The process captures both standard output and standard error.

A successful execution might return:

```json
{
  "output": "Mayukh is 21\n",
  "error": ""
}
```

If the program raises an exception, the error output is returned through `stderr`.

## API

### `POST /run`

Executes the current Python program inside Docker.

#### Request

```json
{
  "input": "Mayukh\n21\n"
}
```

The `input` field is optional.

For a program that does not require input:

```json
{
  "input": ""
}
```

#### Example Program

```python
name = input()
age = int(input())

print(f"Hello {name}")
print(f"You are {age} years old")
```

#### Example Input

```text
John Doe
21
```

#### Example Output

```text
Hello John Doe
You are 21 years old
```

## Project Structure

```text
code-exec/
│
├── main.py
├── program.py
├── Dockerfile
├── pyproject.toml
├── README.md
└── ...
```

### `main.py`

Contains the API and execution logic.

It:

1. Receives the execution request
2. Builds the Docker image
3. Starts a temporary container
4. Passes input through stdin
5. Captures stdout and stderr
6. Returns the result

### `program.py`

Contains the Python code being executed.

### `Dockerfile`

Defines the environment used to execute the program.

Example:

```dockerfile
FROM python:3.12

WORKDIR /code

COPY program.py .

CMD ["python", "program.py"]
```

## Requirements

* Python 3.12+
* Docker
* Docker Desktop on Windows/macOS

## Installation

Clone the repository:

```bash
git clone https://github.com/m4yukh10/code-exec.git
cd code-exec
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Or, if using `uv`:

```bash
uv sync
```

Make sure Docker is running before starting the application.

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Docker Execution

The application relies on Docker for code execution.

Manually building the execution image:

```bash
docker build -t my-python-app .
```

Running it:

```bash
docker run --rm my-python-app
```

For programs that require stdin:

```bash
docker run --rm -i my-python-app
```

The container is removed automatically after the program exits because of `--rm`.

## Execution Model

The project intentionally keeps the execution model simple:

```text
              ┌───────────────┐
              │   Python Code │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  program.py   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ docker build  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Docker Image  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    Container  │
              │               │
              │ Python runs   │
              │     code      │
              └───────┬───────┘
                      │
                stdout/stderr
                      │
                      ▼
              ┌───────────────┐
              │ API Response  │
              └───────────────┘
                      │
                      ▼
              Container removed
```

## Why Docker?

Running arbitrary Python code directly on the host system would allow that code to interact directly with the host environment.

Docker provides a separate execution environment for the program.

For this project, Docker is used to:

* isolate the execution environment
* provide a consistent Python runtime
* keep executed code separate from the host process
* create disposable execution containers

This project is intended as a learning implementation of a container-based code execution system, not as a production-grade sandbox.

## Current Limitations

The current implementation is intentionally simple.

It does not yet provide:

* execution time limits
* CPU limits
* memory limits
* network restrictions
* filesystem restrictions
* multi-user job management
* persistent execution history
* production-grade sandboxing

These can be added as the project evolves.

## Future Improvements

Potential improvements include:

* execution timeouts
* Docker resource limits
* disabled container networking
* read-only container filesystems
* better error handling
* unique execution environments
* frontend code editor
* execution history
* support for additional languages

## Tech Stack

* **Python**
* **FastAPI**
* **Docker**
* **subprocess**
* **Pydantic**

## License

This project is intended for learning and experimentation.
