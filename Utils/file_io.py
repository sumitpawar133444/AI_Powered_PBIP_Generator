import os
import json
import re

def save_specs_to_input_folder(project_name, frontend, backend):
    """
    Saves JSON specifications into a structured Output folder.
    Path: Data/Output/{project_name}/{spec_type}.json
    """
    # 1. Clean the project name to be filesystem-friendly
    safe_name = re.sub(r'[^\w\s-]', '', project_name).strip().replace(" ", "_")

    # 2. Define the path
    project_dir = os.path.join("Data", "Input", safe_name)

    # 3. Create the directory if it doesn't exist
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    # 4. Save Frontend Spec
    with open(os.path.join(project_dir, "frontend_spec.json"), "w") as f:
        json.dump(frontend, f, indent=4)

    # 5. Save Backend Spec
    with open(os.path.join(project_dir, "backend_spec.json"), "w") as f:
        json.dump(backend, f, indent=4)

    return project_dir