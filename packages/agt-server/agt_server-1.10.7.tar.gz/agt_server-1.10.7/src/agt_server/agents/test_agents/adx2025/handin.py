import os
import importlib
import sys
import json
from datetime import datetime
import shutil
from agt_server.local_games.adx_arena import AdXGameSimulator
import re

# Assuming the submissions directory is where the script is located
SUBMISSIONS_DIR = os.path.dirname(__file__)

import os

def add_init_files(directory):
    """
    Recursively creates __init__.py files in every subdirectory of the specified directory,
    ensuring that each directory is recognized as a Python package.
    Hidden directories (starting with '.') are ignored.
    """
    for root, dirs, _ in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for dir in dirs:
            init_file_path = os.path.join(root, dir, '__init__.py')
            open(init_file_path, 'a').close()

def rename_directories(submissions_dir):
    for student_dir_name in os.listdir(submissions_dir):
        student_dir_path = os.path.join(submissions_dir, student_dir_name)
        if os.path.isdir(student_dir_path):
            new_name = student_dir_name.split('@')[0]  # Get the name before '@'
            new_dir_path = os.path.join(submissions_dir, new_name)
            os.rename(student_dir_path, new_dir_path)

def update_python_imports_to_relative(student_dir_path):
    """
    Updates Python files in the specified directory to use relative imports for
    modules that are part of the same submission, but only if the import matches
    a filename in the directory.
    """
    python_files = {file[:-3] for file in os.listdir(student_dir_path) if file.endswith('.py')}
    
    for root, dirs, files in os.walk(student_dir_path):
        for filename in files:
            if filename.endswith('.py'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                with open(file_path, 'w') as file:
                    for line in lines:
                        modified_line = line  
                        simple_import_match = re.match(r'^import (\w+)', line)
                        from_import_match = re.match(r'^from (\w+) import (\w+)', line)
                        if simple_import_match and simple_import_match.group(1) in python_files:
                            modified_line = f"from . import {simple_import_match.group(1)}\n"
                        elif from_import_match and from_import_match.group(1) in python_files:
                            modified_line = f"from .{from_import_match.group(1)} import {from_import_match.group(2)}\n"
                        file.write(modified_line)
    
def clear_directory_contents(student_dir_path):
    """
    Deletes specific files and directories within the specified directory
    and removes all print statements from Python files.
    """
    files_to_delete = ['.gitignore', 'local_elo_ranking.json']
    dirs_to_delete = ['saved_games']
    
    for filename in files_to_delete:
        filepath = os.path.join(student_dir_path, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
    
    for dirname in dirs_to_delete:
        dirpath = os.path.join(student_dir_path, dirname)
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)
    
    # Remove print statements from Python files
    for root, _, files in os.walk(student_dir_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                with open(file_path, 'w') as f:
                    for line in lines:
                        if not re.match(r'\s*print\(.*\)', line):
                            f.write(line)
            
def clear_pycache(directory):
    """
    Recursively deletes __pycache__ directories within the specified directory.
    """
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            
def get_submission_modules(submissions_dir):
    submission_modules = []
    names_counter = {}  
    seen_imports = set()
    
    add_init_files(submissions_dir)  # Ensure all directories are packages
    rename_directories(submissions_dir)
    
    for student_dir_name in set(os.listdir(submissions_dir)):
        student_dir_path = os.path.join(submissions_dir, student_dir_name)
        if os.path.isdir(student_dir_path):
            clear_pycache(student_dir_path)
            for dirpath, _, filenames in os.walk(student_dir_path):
                clear_directory_contents(student_dir_path)
                if 'agent_submission.py' in filenames:
                    update_python_imports_to_relative(dirpath)  # Apply relative imports
                    relative_path = os.path.relpath(dirpath, SUBMISSIONS_DIR).replace(os.path.sep, '.')
                    import_path = f"{relative_path}.agent_submission"
                    break
            try:
                if import_path not in seen_imports: 
                    print(f"Import Path: {import_path}")
                    module = importlib.import_module(import_path)
                    agent_submission = getattr(module, 'agent_submission', None)
                    if agent_submission:
                        mod_time = os.path.getmtime(student_dir_path)
                        agent_submission.timestamp = mod_time
                        original_name = agent_submission.name
                        if original_name in names_counter:
                            names_counter[original_name] += 1
                            agent_submission.name = f"{original_name}({names_counter[original_name]})"
                        else:
                            names_counter[original_name] = 0
                        print(f"IMPORTING {agent_submission.name}")
                        submission_modules.append(agent_submission)
                        seen_imports.add(import_path)
                
            except Exception as e:
                print(f"Failed to import {student_dir_name}: {e}", file=sys.stderr)
            
    return submission_modules

if __name__ == "__main__":
    # Loading configuration from a JSON file
    config_path = os.path.join(SUBMISSIONS_DIR, "config.json")  # Adjust path as necessary
    with open(config_path) as cfile:
        server_config = json.load(cfile)
    
    print(SUBMISSIONS_DIR)
    agent_submissions = get_submission_modules(SUBMISSIONS_DIR)
    print(f"{len(agent_submissions)} successfully imported")
    print([agent.name for agent in agent_submissions if agent is not None])
    
    
    start = datetime.now()
    
    arena = AdXGameSimulator(save_path=server_config['save_path'], 
                             local_save_path=server_config['local_save_path'])
    arena.run_simulation(agents=agent_submissions, num_simulations=500)
    end = datetime.now()
    print(f"Time Elapsed (s): {(end - start).total_seconds()}")
