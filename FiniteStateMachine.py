from FSM_components import FSM
from AddedActions import Actions

# Correct inputs
exp1 = "d =a*((b)+ c)*d+1|"
exp2 = "abs= ((pos) + 12.45) *(14e+3 + num)|"
exp3 = "abs = (pos)|"
exp4 = "d =a*((b)+ c)*11e+5+1|"
exp5 = "cost  =  (price+(Tax))*0.98|"
exp6 = "   d =  (  (a * ( ( 0.012 + 7E+50 ) )) +((dom)* 228)  )|"
exp7 = "d =a*((b)+ c)*d+1|"
exp8 = "abs = 3.5*((x+66E-5))+y34|"
# Incorrect inputs
exp9 = "abs = 5num+80"
exp10 = "abs = num + em12e-5"
exp11 = "abs =    |"
exp12 = "abs|"
exp13 = "  abs (=a(*b"
exp14 = "abs =a(*b"
exp15 = "abs =a*)b"
exp16 = "abs =(a*(b)"
exp17 = "abs = (10+x)*y+0.98*(price+tax)|"

EXPRESSION = exp17


def main():
    q_count, alphabet, transitions = FSM.parse_file("input.txt")
    fsm = FSM(q_count, alphabet)
    actions = Actions()
    fsm.transitions_table = transitions
    # fsm.transitions_table
    if fsm.execute(EXPRESSION, actions):
        RPN_to_code(fsm.rpn)
        optimized_code()



def RPN_to_code(rpn):  # Перевод из ОПЗ в псевдакод
    cr, cl = 0, 0
    stack = []
    for elem in rpn:
        if elem not in ["+", "*", "="]:
            try:
                int(elem)
                stack.append("=" + elem)
            except ValueError:
                try:
                    float(elem)
                    stack.append("=" + elem)
                except ValueError:
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
