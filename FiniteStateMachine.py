from FSM_components import FSM
from AddedActions import Actions


def main():
    # exp = "d =a*((b)+ c)*d+1|"
    # exp = "abs= ((pos) + 12.45) *(14e-3 + num)|"
    # exp = "abs = (pos)|"
    # exp = "d =a*((b)+ c)*11e+5+1|"
    # exp = "d =x*(a+b)+y|"
    exp = "cost  =  (price+(Tax))*0.98|"
    # exp = "   d =  (  (a * ( ( 0.012 + 7E+50 ) )) +((dom)* 228)  )|"
    # "d =a*((b)+ c)*d+1|"
    # "abs = 3.5*((x+66E-5))+y34|"

    q_count, alphabet, transitions = FSM.parse_file("input.txt")
    fsm = FSM(q_count, alphabet)
    actions = Actions()
    fsm.transitions_table = transitions
    # fsm.transitions_table
    if fsm.execute(exp, actions):
        RPN_to_optimized_code(fsm.rpn)


def RPN_to_optimized_code(rpn):  # Перевод из ОПЗ в псевдакод
    cr, cl = 0, 0
    stack = []
    for elem in rpn:
        if elem not in ["+", "*", "="]:
            stack.append(elem)
        elif elem == "+":
            cr = stack.pop()
            cl = stack.pop()
            if cr.find("$") != -1 and cl.find("$") != -1:
                index_num = max(int(cr[cr.find("$") + 1]), int(cl[cl.find("$") + 1])) + 1
            elif cr.find("$") != -1:
                index_num = int(cr[cr.find("$") + 1]) + 1
            elif cl.find("$") != -1:
                index_num = int(cl[cl.find("$") + 1]) + 1
            else:
                index_num = 1
            add_template = f"{cr}\nSTORE ${index_num}\nLOAD {cl}\nADD ${index_num}"
            stack.append(add_template)
        elif elem == "*":
            cr = stack.pop()
            cl = stack.pop()
            if cr.find("$") != -1 and cl.find("$") != -1:
                index_num = max(int(cr[cr.find("$") + 1]), int(cl[cl.find("$") + 1])) + 1
            elif cr.find("$") != -1:
                index_num = int(cr[cr.find("$") + 1]) + 1
            elif cl.find("$") != -1:
                index_num = int(cl[cl.find("$") + 1]) + 1
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


if __name__ == "__main__":
    main()
