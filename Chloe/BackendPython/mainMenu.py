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
                    return match.group(2).strip()
                else:
                    return line.strip()
    return None


#if __name__ == "__main__":
#    path = "../static/lessons/lesson1.txt"
#    print(readTypesOfLines(path))
#    print(readLine(path, 1))