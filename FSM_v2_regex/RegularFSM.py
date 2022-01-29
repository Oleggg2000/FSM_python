import regex

# Correct inputs
exp1 = "abs= ((pos) + 12.45) *(14e+3 + num)"
exp2 = "abs = (pos)"
exp3 = "d =a*((b)+ c)*11e+5+1"
exp4 = "   d =  (  (a * ( ( 0.012 + 7E-50 ) )) +((dom)* 228)  )"
exp5 = "d =a*((b)+ c)*d+1"
exp6 = "d =x*a+b+y"
exp7 = "cost  =  (price+(Tax))*0.98"
exp8 = "d =a*((b)+ c)*d+1"
exp9 = "abs = 3.5*((x+66E-5))+y34"
# Incorrect inputs
exp10 = "abs = 5num+80"
exp11 = "abs = num + em12e-5"
exp12 = "abs =  4+ "
exp13 = "abs"
exp14 = "  abs (=a(*b"
exp15 = "abs =a*)b"
exp16 = "abs =(a*(b)"
exp17 = "abs =a*Tat+*b"
exp18 = "abs =a*023.12+b"

EXPRESSION = exp7


def main():
    try:
        vars, signs = exec()
        # print(vars, signs, sep="\n")
        rpn = to_rpn(vars, signs)
        RPN_to_optimized_code(rpn)
        optimized_code()
    except TypeError:
        pass


def exec():
    id_pattern = r"(?P<var>[a-zA-Z_]+\w*)"
    var_pattern = r"(?<=[*+=\s(])(?P<var>\d+[eE][-+]\d+|[a-zA-Z_]+\w*|(?:0\.|[1-9]+)\.?[0-9]*)(?=\s*[+*)]|)"
    sign_pattern = r"(?P<sign>[=+*])"
    ob_pattern = r"(?:(?P<sign>\()|\s)"  # opened bracket pattern
    cb_pattern = r"(?:(?P<sign>\))|\s)"  # closed bracket pattern

    exp_pattern = fr"\s*{id_pattern}\s*(?P<sign>=)(?:{ob_pattern}*{var_pattern}{cb_pattern}*{sign_pattern}?{ob_pattern}*)+"

    m = regex.match(exp_pattern, EXPRESSION)
    # print(m.group(0))
    # print(m.capturesdict(), "\n")

    # Ошибка до присвоения
    if m is None:
        print(f'"{EXPRESSION}"\n' + " " * (EXPRESSION.find("=")) + "^ Error occurred before assignment!")
    # Есле в группе 0 не лежит все выражение, то вывести где прервалась ругулярка
    elif len(m.group(0)) != len(EXPRESSION):
        error = len(m.group())
        print(f'{EXPRESSION}\n' + " " * error + "^ Error occurred")
    # Проверка на балансировку скобок
    elif EXPRESSION.count("(") != EXPRESSION.count(")"):
        print(f"{EXPRESSION}\nWrong amount of brackets!")
    # Входная цепочка верна
    elif EXPRESSION.strip()[-1] not in ["+", "*", "="]:
        print(f'"{m.group(0)}"\nExpression is an acceptable!')
        return m.capturesdict()["var"], m.capturesdict()["sign"]
    # Последний символ знак, ошибка!
    else:
        print(f'{EXPRESSION}\n' + " " * (len(m.group())-1) + "^ Error occurred")


def to_rpn(vars, signs):
    i_sign = 0
    priority = ["=", "(", "+", "*"]
    stack = []
    rpn = []
    vars.reverse()
    rpn.append(vars.pop())
    for i in range(len(signs)):
        if signs[i] in ["+", "*", "="]:

            if len(stack) == 0 or priority.index(stack[len(stack) - 1]) < priority.index(signs[i]):
                stack.append(signs[i])
            else:
                while len(stack) != 0 and priority.index(stack[len(stack) - 1]) >= priority.index(signs[i]):
                    rpn.append(stack.pop())
                stack.append(signs[i])
        elif signs[i] == "(":
            stack.append(signs[i])
        elif signs[i] == ")":
            stack_elem = stack.pop()
            rpn.append(stack_elem)
            while stack_elem != "(":
                stack_elem = stack.pop()
                rpn.append(stack_elem)
            rpn.pop()

        if signs[i] in ["+", "*", "="]:
            rpn.append(vars.pop())

    while stack:
        rpn.append(stack.pop())
    print("Reverse Polish notation: " + "  ".join(elem for elem in rpn))
    if "(" in EXPRESSION:
        print("Table of names: ) ( " + " ".join(elem for elem in set(rpn)))
    else:
        print("Table of names: " + " ".join(elem for elem in set(rpn)))
    return rpn


def RPN_to_optimized_code(rpn):  # Перевод из ОПЗ в псевдакод
    cr, cl = 0, 0
    stack = []
    for elem in rpn:
        if elem not in ["+", "*", "="]:
            stack.append(elem)
        elif elem == "+":
            cr = stack.pop()
            cl = stack.pop()
            if cr.rfind("$") != -1 and cl.rfind("$") != -1:
                index_num = max(int(cr[cr.rfind("$") + 1]), int(cl[cl.rfind("$") + 1])) + 1
            elif cr.rfind("$") != -1:
                index_num = int(cr[cr.rfind("$") + 1]) + 1
            elif cl.rfind("$") != -1:
                index_num = int(cl[cl.rfind("$") + 1]) + 1
            else:
                index_num = 1
            add_template = f"{cr}\nSTORE ${index_num}\nLOAD {cl}\nADD ${index_num}"
            stack.append(add_template)
        elif elem == "*":
            cr = stack.pop()
            cl = stack.pop()
            if cr.rfind("$") != -1 and cl.rfind("$") != -1:
                index_num = max(int(cr[cr.rfind("$") + 1]), int(cl[cl.rfind("$") + 1])) + 1
            elif cr.rfind("$") != -1:
                index_num = int(cr[cr.rfind("$") + 1]) + 1
            elif cl.rfind("$") != -1:
                index_num = int(cl[cl.rfind("$") + 1]) + 1
            else:
                index_num = 1
            mpy_template = f"{cr}\nSTORE ${index_num}\nLOAD {cl}\nMPY ${index_num}"
            stack.append(mpy_template)
        elif elem == "=":
            cr = stack.pop()
            cl = stack.pop()
            assign_template = f"LOAD {cr}\nSTORE {cl}"
    with open("output.txt", mode="w") as f:
        f.write(assign_template)

def optimized_code():
    with open("output.txt", mode="r") as f:
        code = f.read().split("\n")
    # print(code)

    while True:
        i = 0
        temp = code.copy()
        for i in range(len(code)-2):
            if "STORE" in code[i] and "LOAD" in code[i+1] and ("ADD" in code[i+2] or "MPY" in code[i+2]):
                temp_str = code[i+1][4:]
                code[i+1] = code[i+1][:4] + code[i+2][3:]
                code[i+2] = code[i+2][:3] + temp_str
                if code[i][5:] == code[i+1][4:]:
                    code.pop(i)
                    code.pop(i)
                    break
                else:
                    temp = code.copy()
            elif "LOAD" in code[i] and "STORE" in code[i + 1] and "LOAD" in code[i+2]:
                for j in range(i+2, len(code)):
                    if code[i+1][5:] in code[j]:
                        code[j] = code[j].replace(code[i+1][5:], code[i][4:])
                code.pop(i)
                code.pop(i)
                break
        if temp == code:
            break
    with open("output.txt", mode="w") as f:
        while code:
            f.write(code.pop(0) + "\n")


if __name__ == "__main__":
    main()
