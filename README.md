
# CmdAI

A small command line tool to create short Python scripts that solve a very specific problem.

## Tools

### cai (Command AI)

Usage: cai <prompt>

This will generate a cai_script.py in the current directory which should implement what was requested for in the prompt. Cai can make use in it's scripts of a function that uses AI, called tai(p), when it thinks it needs it.

Example: cai "generate a txt summary of files in the current folder and their byte size"

This generated a cai_script.py that does exactly what the prompt says, here's the code Gemini generated:

```python
# Import the 'os' module for interacting with the operating system
import os

# The tai function is expected to be provided by the execution environment.
# It takes a string prompt and returns an AI-generated string.

def generate_file_summary():
    """
    Generates a summary of files in the current folder, including their names and byte sizes,
    and writes this summary to a text file with a TAI-generated name.
    """
    print("Starting script: Generate file summary.")

    # Get the current working directory
    current_directory = os.getcwd()
    print(f"Scanning directory: {current_directory}")

    # List all entries (files and directories) in the current directory
    try:
        entries = os.listdir(current_directory)
    except OSError as e:
        print(f"Error: Could not list directory '{current_directory}'. Details: {e}")
        return

    file_details = []
    print("Gathering file information...")

    # Iterate over each entry to find files and their sizes
    for entry_name in entries:
        full_path = os.path.join(current_directory, entry_name)

        # Check if the entry is a file (not a directory)
        if os.path.isfile(full_path):
            try:
                file_size = os.path.getsize(full_path)
                file_details.append({"name": entry_name, "size": file_size})
                print(f"  - Found file: {entry_name}, Size: {file_size} bytes")
            except OSError as e:
                print(f"  - Warning: Could not get size for file '{entry_name}'. Details: {e}")

    # Prepare the summary content header
    print("Requesting current date and time from TAI for the report header.")
    current_datetime_str = tai("Provide the current date and time in a human-readable format (e.g., YYYY-MM-DD HH:MM:SS or Month Day, Year, HH:MM AM/PM).")
    summary_intro = f"File Summary Report\nDirectory: {current_directory}\nGenerated on: {current_datetime_str}\n\n"

    if not file_details:
        print("No files found in the current directory to summarize.")
        summary_content = summary_intro + "No files were found in this directory."
    else:
        header = f"{'Filename':<60} {'Size (bytes)':>15}\n"
        separator = "-" * 77 + "\n"
        
        file_lines_str = ""
        for detail in file_details:
            filename_display = detail['name']
            if len(filename_display) > 57:
                filename_display = filename_display[:57] + "..."
            file_lines_str += f"{filename_display:<60} {detail['size']:>15}\n"
        
        summary_content = summary_intro + header + separator + file_lines_str + separator
        print("File summary content prepared.")

    # Generate a name for the summary TXT file using TAI
    summary_filename_prompt = "Generate a concise and suitable filename for a text file that summarizes files and their sizes. The filename must end with '.txt' and be a single valid filename string, without any path components or quotes. Examples: 'FileAndSizeReport.txt', 'DirectoryScanSummary.txt'."
    print(f"Requesting filename from TAI with prompt: \"{summary_filename_prompt}\"")
    summary_filename = tai(summary_filename_prompt)
    
    print(f"TAI suggested filename: '{summary_filename}'")
    # Sanitize the filename received from TAI
    # 1. Remove leading/trailing whitespace and quotes (single or double)
    summary_filename = summary_filename.strip().strip('\'"')

    # 2. Handle empty or effectively empty filename from TAI
    if not summary_filename:
        print("TAI returned an empty filename. Using default: 'file_summary_report.txt'")
        summary_filename = "file_summary_report.txt"
    else:
        # 3. Ensure it ends with .txt
        if not summary_filename.lower().endswith(".txt"):
            base, ext = os.path.splitext(summary_filename)
            if ext: # Has non-.txt extension
                 summary_filename += ".txt" # e.g. report.log -> report.log.txt
            else: # No extension or TAI gave one without a dot
                 summary_filename = base + ".txt" # e.g. report -> report.txt

        # 4. Replace common invalid characters for Windows filenames
        invalid_os_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char_to_replace in invalid_os_chars:
            summary_filename = summary_filename.replace(char_to_replace, '_')

        # 5. Final check for problematic names (e.g., just ".txt", or became empty after sanitization)
        test_name = summary_filename.replace('.', '').replace('_', '').strip()
        if not test_name or summary_filename == ".txt":
            print(f"Sanitized filename ('{summary_filename}') is invalid. Using default: 'file_summary_report.txt'")
            summary_filename = "file_summary_report.txt"
    
    print(f"Final filename for summary: '{summary_filename}'")

    # Write the summary to the TXT file
    output_file_path = os.path.join(current_directory, summary_filename)
    try:
        print(f"Attempting to write summary to: '{output_file_path}'")
        with open(output_file_path, "w", encoding="utf-8") as summary_file_object:
            summary_file_object.write(summary_content)
        print(f"Summary successfully written to '{output_file_path}'")
    except IOError as e:
        print(f"Error: Could not write summary to file '{output_file_path}'. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing the file '{output_file_path}': {e}")

# Standard boilerplate to call the main function
if __name__ == "__main__":
    generate_file_summary()
```

Sometimes, like in this example, cai generates an excesively long script, or innecessarily includes tai, but since this tool is for in-the-moment needs, this is usually not a problem.

### tai (Text AI)

Usage: tai <prompt>

This is a command line program that simply retrieves a response of some AI model for the given prompt, and outputs that response to the terminal.

Example: tai "What is round, white, edible, small?"
Response: Marshmellow

Example: tai "list of costarrican provinces"
Response: San José, Alajuela, Cartago, Heredia, Guanacaste, Puntarenas, Limón

This allows integrating AI in batch/command-line scripts to make decisions, generate content, or whatever you like.

## To use

Create a venv, pip install google.generativeai.

## License

I retain any rights to this code that I am able to. It's not amazing code anyway.
