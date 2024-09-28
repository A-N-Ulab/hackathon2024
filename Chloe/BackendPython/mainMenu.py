import re

def readTypesOfLines(path):
    types_of_lines = []
    with open(path, 'r') as file:
        for line in file:
            match = re.match(r'^(.*?):', line)
            if match:
                types_of_lines.append(match.group(1))
    return types_of_lines

def readLine(path, lineNum):
    with open(path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == lineNum:
                match = re.match(r'^(.*?):(.*)', line)
                if match:
                    return match.group(2).strip()
                else:
                    return line.strip()
    return None
