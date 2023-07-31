import os, subprocess, sys, pyflakes.api

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
class PyflakesImplementation(interface.StaticCodeAnylazer):
    def scan_file(directory_path, output_path):
       
        report = pyflakes.api.Report()

        # Run Pyflakes on the specified directory
        try:
            pyflakes.api.checkRecursive(directory_path, report)
        except Exception as e:
            print(f"Error running Pyflakes: {e}")
            return False

        # Write the Pyflakes analysis results to the output file
        try:
            with open(output_path, 'w') as output_file:
                for warning in report:
                    output_file.write(str(warning) + '\n')
            print(f"Pyflakes analysis completed successfully. Results saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error writing to output file: {e}")
            return False

    if __name__ == "__main__":
        directory_path = "./my_project"
        output_path = "./pyflakes_results.txt"

        success = scan_file(directory_path, output_path)
        if not success:
            print("Pyflakes analysis failed.")








   