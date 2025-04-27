import os
from huggingface_hub import hf_hub_download, create_repo, upload_file, login

from ._utils import load_model_low, load_hf_low
from .debug import debug_state
from .independent import SetUpAPI

@debug_state.trace_func
def load_model(path,dtype= None):
    return load_model_low(path,dtype)

@debug_state.trace_func
def load_hf(path,dtype= None):
    return load_hf_low(path,dtype)

@debug_state.trace_func
def push_model(repo_name, folder_path):
    files_to_upload = ["good_stuff.pkl", "understanding_good_stuff.json","make_stuff_better.pkl"]
    
    create_repo(repo_name, exist_ok=True)  # Create repo if it doesn’t exist

    for file_name in files_to_upload:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only upload if the file exists
            upload_file(
                path_or_fileobj=file_path,
                path_in_repo=file_name,  # Save with the same filename
                repo_id=repo_name,
                repo_type="model",
            )
    print(f"Uploaded {files_to_upload} to {repo_name}")