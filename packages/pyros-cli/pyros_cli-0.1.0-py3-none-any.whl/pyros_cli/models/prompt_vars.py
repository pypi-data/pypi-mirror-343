import os
from typing import Optional
from pydantic import BaseModel

from pyros_cli.globals import CURRENT_DIR


class PromptVars(BaseModel):
    file_path: Optional[str] = None
    prompt_id: Optional[str] = None
    description: Optional[str] = None
    values: list[str] = []



def load_prompt_vars() -> dict[str, PromptVars]:
    """Load prompt variables from the library/prompt_vars directory"""

    # Get the absolute path to the prompt_vars directory
    prompt_vars_dir = os.path.abspath(os.path.join(CURRENT_DIR, "library/prompt_vars"))

    prompt_vars = {}
    if not os.path.exists(prompt_vars_dir):
        return prompt_vars
    
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(prompt_vars_dir):
        for file in files:
            # Check for both .md and .txt files
            if file.endswith((".md", ".txt")):
                # Get the relative path from the prompt_vars directory
                rel_path = os.path.relpath(root, prompt_vars_dir)
                file_path = os.path.join(root, file)
                
                # Create the prompt_id with subfolder path if not in root directory
                if rel_path == ".":
                    # File is in the root directory
                    prompt_id = f"__{os.path.splitext(file)[0]}__"
                else:
                    # File is in a subdirectory
                    prompt_id = f"__{os.path.join(rel_path, os.path.splitext(file)[0])}__"
                
                # Replace backslashes with forward slashes for cross-platform compatibility
                prompt_id = prompt_id.replace("\\", "/")
                
                description_lines = []
                values = []
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            elif line.startswith("#"):
                                description_lines.append(line)
                            else:
                                values.append(line)
                    
                    description = "\n".join(description_lines) if description_lines else None
                    
                    prompt_vars[prompt_id] = PromptVars(
                        file_path=file_path,
                        prompt_id=prompt_id,
                        description=description,
                        values=values
                    )
                except UnicodeDecodeError:
                    # Try with a fallback encoding
                    try:
                        with open(file_path, "r", encoding="latin-1") as f:
                            content = f.read()
                        
                        # Process the content line by line
                        for line in content.splitlines():
                            line = line.strip()
                            if not line:
                                continue
                            elif line.startswith("#"):
                                description_lines.append(line)
                            else:
                                values.append(line)
                        
                        description = "\n".join(description_lines) if description_lines else None
                        
                        prompt_vars[prompt_id] = PromptVars(
                            file_path=file_path,
                            prompt_id=prompt_id,
                            description=description,
                            values=values
                        )
                    except Exception as e:
                        print(f"Error loading prompt file {file_path}: {e}")
                except Exception as e:
                    print(f"Error loading prompt file {file_path}: {e}")
                
    return prompt_vars
