import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        output_string = ""
        command = ["python", os.path.abspath(target_dir)]
        if args is not None:
            command.extend(args)
        complete = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=abs_working_dir)
        if not complete.returncode == 0:
            output_string += f"Process exited with code {complete.returncode}."
        if complete.stdout == "" and complete.stderr == "":
            output_string += "No output produced."
        else:
            if complete.stdout != "":
                 output_string += f" STDOUT: {complete.stdout}"
            if complete.stderr != "":
                output_string += f" STDERR: {complete.stderr}"
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file, evaluates if program runs, returns associated exit code or string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run python from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Arguments used for the python script, if any.",
                },
            },
            "required": ["file_path"], 
        },
    },
}