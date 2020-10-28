import sys

file_name = sys.argv[1].split("\\")[-1][0:-3]

segment_labels = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"
}
   
def push(parts):
    if parts[1] == "constant":
        return (f"@{parts[2]}\n"
               "D=A\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n")
    elif parts[1] == "temp":
        return (
            f"@R{5+int(parts[2])}\n"
            "D=M\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
    elif parts[1] == "pointer":
        return (
            f"@R{3+int(parts[2])}\n"
            "D=M\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
    elif parts[1] != "static":
        return (
            f"@{parts[2]}\n"
            "D=A\n"
            f"@{segment_labels[parts[1]]}\n" 
            "A=M+D\n"
            "D=M\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
    else:
        return (
            f"@{file_name}.{parts[2]}\n"
            "D=M\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
     
def pop(parts):
    if parts[1] == "temp":
        return (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@R{5+int(parts[2])}\n"
            "M=D\n"
        )
    elif parts[1] == "pointer":
        return (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@R{3+int(parts[2])}\n"
            "M=D\n"
        )
    elif parts[1] != "static":
        return (
            f"@{parts[2]}\n"
            "D=A\n"
            f"@{segment_labels[parts[1]]}\n"
            "M=M+D\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{segment_labels[parts[1]]}\n"
            "A=M\n"
            "M=D\n"
            f"@{parts[2]}\n"
            "D=A\n"
            f"@{segment_labels[parts[1]]}\n"
            "M=M-D\n"
        )
    else:
        return (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{file_name}.{parts[2]}\n"
            "M=D\n"
        )

add = (
    "@SP\n"
    "AM=M-1\n"
    "D=M\n"
    "A=A-1\n"
    "M=M+D\n"
)

neg = (
    "@SP\n"
    "A=M-1\n"
    "M=-M\n"
)

sub = (
    "@SP\n"
    "AM=M-1\n"
    "D=M\n"
    "A=A-1\n"
    "M=M-D\n"
)

logic_not = (
    "@SP\n"
    "A=M-1\n"
    "M=!M\n"
)

logic_and = (
    "@SP\n"
    "AM=M-1\n"
    "D=M\n"
    "A=A-1\n"
    "M=D&M\n"
)

logic_or = (
    "@SP\n"
    "AM=M-1\n"
    "D=M\n"
    "A=A-1\n"
    "M=D|M\n"
)

operations = {
    "add": add,
    "sub": sub,
    "neg": neg,
    "and": logic_and,
    "or" : logic_or,
    "not": logic_not
}

label_counter = 0
def comparision(operator):
    global label_counter
    temp = sub
    comparision_table = {
        "eq": ["EQUAL", "JEQ", "NOT_EQUAL", "JNE"],
        "gt": ["GREATER", "JGT", "NOT_GREATER", "JLE"],
        "lt": ["SMALLER", "JLT", "NOT_SMALLER", "JGE"]   
    }
    
    type_a = comparision_table[operator][0]
    jump_a = comparision_table[operator][1]
    type_b = comparision_table[operator][2]
    jump_b = comparision_table[operator][3]
    
    temp += ("@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{type_a}_{label_counter}\n" 
            f"D;{jump_a}\n" 
            f"@{type_b}_{label_counter}\n"
            f"D;{jump_b}\n" 
            f"({type_a}_{label_counter})\n"
            "@SP\n"
            "A=M\n"
            "M=-1\n"
            f"@NEXT_{label_counter}\n"
            "0;JMP\n"
            f"({type_b}_{label_counter})\n"
            "@SP\n"
            "A=M\n"
            "M=0\n"
            f"(NEXT_{label_counter})\n"
            "@SP\n"
            "M=M+1\n")
    return temp

def parser(text):
    global label_counter
    target = ""
    for line in text:
        parts = line.split()
        if parts[0] == "push":
            target += push(parts)
        elif parts[0] == "pop":
            target += pop(parts)
        elif parts[0] not in ["eq", "gt", "lt"]:
            target += operations[parts[0]]
        else:
            target += comparision(parts[0])
            label_counter += 1
    return target

def translate():
    path = sys.argv[1]

    f_raw = []
    with open(path) as f:
        for line_no, line_content in enumerate(f):
            f_raw.append([line_no, line_content])
    
    f_content = []
    # clean comments
    for line in f_raw:
        if line[1][0:2] not in ["//", "\n"]:
            if line[1][-1:] == "\n":
                f_content.append(line[1][0:-1])
            else:
                f_content.append(line[1])

    translated_content = parser(f_content)

    new_file = path[0:len(path)-2] + "asm"
    with open(new_file, "w") as f:
        f.write(translated_content)
    print("success")
    
translate()
        
# D:\Programming\nand2tetris\projects\07\StackArithmetic\SimpleAdd\SimpleAdd.vm
# D:\Programming\nand2tetris\projects\07\StackArithmetic\StackTest\StackTest.vm
# D:\Programming\nand2tetris\projects\07\MemoryAccess\BasicTest\BasicTest.vm
# D:\Programming\nand2tetris\projects\07\MemoryAccess\PointerTest\PointerTest.vm