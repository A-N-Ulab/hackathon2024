import re

# Specify the path to your file
file_path = 'content.txt'  # Change this to your actual file path

try:
    # Open the file in read mode with UTF-8 encoding , encoding='utf-8'
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except IOError:
    print(f"Error: An I/O error occurred while reading the file '{file_path}'.")

# Split the content into sections based on 'section' keyword
sections = re.split(r'section\((.*?)\)', content)[1:]  # Skip the first empty element

# Process each section
for index in range(0, len(sections), 2):
    section_title = sections[index].strip()
    section_content = sections[index + 1].strip()

    print(f"Section: {section_title}\n")

    # Find all relevant information within the section content
    subject_match = re.search(r'Subject:\s*(.*)', section_content)
    info_matches = re.findall(r'Info:\s*(.*?)(?=\n|$)', section_content, re.DOTALL)
    task_matches = re.findall(r'Task:\s*(.*?)(?=\n|$)', section_content)

    if subject_match:
        print(f"  Subject: {subject_match.group(1).strip()}")

    if info_matches:
        for i, info in enumerate(info_matches, start=1):
            print(f"  Info {i}: {info.strip()}")

    if task_matches:
        for j, task in enumerate(task_matches, start=1):
            answer = re.findall(r':\s*(.*)(?=\n|$)', task)
            
            print(f"  Task {j}: {task.strip()}")
            print(f"  Answer {j}: {answer[0].strip()}")

    #print()  # Print a newline for better readability



# Call the function to parse the content
#parse_content(file_path)