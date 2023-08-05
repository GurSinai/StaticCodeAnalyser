import os, subprocess, sys, pyflakes.api

### Import Interface Module
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory path to sys.path
sys.path.append(parent_directory)
import interface
 
class PyflakesImplementation(interface.StaticCodeAnylazer):
    def scan_file(self, file_name, output_path):
       
        report = pyflakes.api.Report()

        # Run Pyflakes on the specified directory
        try:
            pyflakes.api.check(file_name, report)
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



   