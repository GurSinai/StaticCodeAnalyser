import os, subprocess, sys
from LLM.LLM import get_local_name

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
class Flake8Implementation(interface.StaticCodeAnylazer):
    def scan_file(directory_path, output_path):
  
        # Run Flake8 using subprocess
        command = ['flake8', directory_path, '--output-file', output_path]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Flake8 analysis completed successfully. Results saved to: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running Flake8: {e.stderr}")
            return False
    if __name__ == "__main__":
        directory_path = "./{get_local_name}/Flake8"
        output_path = "./flake8_results.txt"

        success = scan_file(directory_path, output_path)
        if not success:
            print("Flake8 analysis failed.")
    
    
        