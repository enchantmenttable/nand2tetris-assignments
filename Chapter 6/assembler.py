import sys

table_comp = {
    "0"  : "0101010",
    "1"  : "0111111",
    "-1" : "0111010",
    "D"  : "0001100",
    "A"  : "0110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "-D" : "0001111",
    "-A" : "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    
    "M"  : "1110000",
    "!M" : "1110001",
    "-M" : "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

table_dest = {
    "M"  : "001",
    "D"  : "010",
    "MD" : "011",
    "A"  : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD": "111"
}

table_jump = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

predefined_symbols = {
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
    "SCREEN": "16384",
    "KBD": "24576"
}

path = sys.argv[1]

with open(path) as f:
    raw_text = []
    for line_no, line_text in enumerate(f):
        raw_text.append([line_no, line_text])

text = []
for line in raw_text:
    # clean whitespace
    if " " in line[1]:
        line[1] = line[1].replace(" ", "")
    if line[1][0:2] not in ["//", "\n"]:
        text.append(line)

i = 0
while i < len(text):
    # re-index
    text[i][0] = i
    
    # delete from "//" onward
    if "//" in text[i][1]:
        text[i][1] = text[i][1][0:( text[i][1].find("//") )]
        
    # delete "\n"
    if "\n" in text[i][1]:
        text[i][1] = text[i][1][0:len(text[i][1])-1]
    
    i += 1

labels = {}
counter = 0
for line in text:
    if line[1][0] == "(":
        labels[line[1][1:-1]] = line[0] - counter
        counter += 1

text_cleaned = []
index = 0
for line in text:
    if "(" not in line[1]:
        text_cleaned.append([index, line[1]])
        index += 1

custom_variables = {}
ram = 16
for line in text_cleaned:
    # convert A-ins to bin
    if line[1][0] == "@":
        if line[1][1:] in predefined_symbols:
            line[1] = predefined_symbols[line[1][1:]]
        elif line[1][1] == "R" and line[1][2:].isdigit():
            line[1] = line[1][2:]    
        elif line[1][1].isdigit():
            line[1] = line[1][1:]
        elif line[1][1:] in labels:
            line[1] = labels[line[1][1:]]
        elif line[1][1:] in custom_variables:
            line[1] = custom_variables[line[1][1:]]
        else:
            custom_variables[line[1][1:]] = ram
            line[1] = ram
            ram += 1
        line[1] = "{0:016b}".format(int(line[1]))
    # convert C-ins to bin
    else:
        if ";" in line[1]: 
            j_ins = line[1][ line[1].find(";")+1: ]
            line[1] = "111" + table_comp[ line[1][0] ] + "000" + table_jump[j_ins]
        if "=" in line[1]:
            c_ins = line[1][ line[1].find("=")+1: ]
            line[1] = "111" + table_comp[c_ins] + table_dest[ line[1][0:line[1].find("=")] ] + "000"

file_content = ""
for line in text_cleaned:
    file_content += line[1] + "\n"

file_name = path.split("/")[-1]
file_name = file_name[0:len(file_name)-3] + "hack"

with open(file_name, "w") as f:
    f.write(file_content)


# D:/Programming/nand2tetris/projects/06/add/Add.asm
# D:/Programming/nand2tetris/projects/06/max/max_test.asm