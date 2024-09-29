import re
from collections import Counter

def readTypesOfLines(path):
    word_counter = Counter()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'^(.*?):(.*)', line)
            if match:
                key = match.group(1).strip()
                word_counter[key] += 1
    return dict(word_counter)

def readLine(path, lineNum):
    with open(path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == lineNum:
                match = re.match(r'^(.*?):(.*)', line)
                if match:
                    content = match.group(2).strip()
                    parts = content.split('_', 1)
                    if len(parts) > 1:
                        return parts[0].strip()
                    else:
                        return content
                else:
                    parts = line.split('_', 1)
                    if len(parts) > 1:
                        return parts[0].strip()
                    else:
                        return line.strip()
    return None

def readStringAfterUnderscore(path, lineNum):
    try:
        with open(path, 'r') as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == lineNum:
                    parts = line.split('_', 1)
                    if len(parts) > 1:
                        return parts[1].strip()
                    else:
                        return None
        return None
    except:
        return None

def extractTextAfterColon(text):
    match = re.match(r'^(.*?);(.*)', text)
    if match:
        return match.group(2).strip()
    return None

#if __name__ == "__main__":
#    path = "./static/lessons/lesson1.txt"
#    print(readTypesOfLines(path))
#    print(readLine(path, 1))
#    print(readStringAfterUnderscore(path, 4))
#    print(extractTextAfterColon(readLine(path, 1)))