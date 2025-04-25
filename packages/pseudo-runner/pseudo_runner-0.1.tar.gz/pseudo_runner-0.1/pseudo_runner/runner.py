import tempfile
import subprocess

def execute_python_code(code):
    """
    Executes the generated Python code by writing it to a temporary file.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    print(f"Executing generated Python code from: {tmp_path}")
    subprocess.run(["python3", tmp_path])