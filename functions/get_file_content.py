import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000
        with open(target_dir, "r") as f:
            file_string = f.read(MAX_CHARS)
            if f.read(1):
                file_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_string

        
    
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns content in a file in a specified directory relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get content from, relative to the working directory.",
                },
            },
            "required": ["file_path"], 
        },
    },
}