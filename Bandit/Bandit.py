import os, subprocess, sys
from LLM.LLM import get_local_name

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
class BanditImplementation(interface.StaticCodeAnylazer):
    def scan_file(directory_path, output_path):
        
        if not os.path.exists(directory_path):
            print(f"Directory '{directory_path}' does not exist.")
            return False

        command = ['bandit', '-r', directory_path, '-o', output_path]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Bandit scan completed successfully. Results saved to: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running Bandit: {e.stderr}")
            return False
    if __name__ == "__main__":
            directory_path = "./{get_local_name}/Bandit"
            output_path = "./bandit_results.txt"

            success = scan_file(directory_path, output_path)
            if not success:
                print("Bandit scan failed.")
