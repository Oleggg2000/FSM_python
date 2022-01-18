import re
from FSM_components import FSM
from AddedActions import Actions


class Passed(Exception):
    pass


class Completed(Exception):
    def __init__(self, ch=0):
        if ch != 0:
            print("Expression is an acceptable!")


def check_for_action(act, len, pos):  # Проверка на наличие внедренных действий
    if act is not None and len > 1:
        if pos[1] == "1":
            act.action1()
        elif pos[1] == "2":
            act.action2()


def main():
    with open("input.txt") as f:
        transitions = []
        q_count = int(f.readline())
        alphabet = f.readline()[0:-1].split("|")
        for line in f:
            line_list = line[0:-1].split("~")
            line_list = [elem.split("|") for elem in line_list]
            transitions.append(line_list)
        print(q_count, alphabet, transitions)

    # exp = "d =a*((b)+ c)*d+1|"
    # exp = "abs= ((pos) + 12.45) *(14e-3 + num)|"
    # exp = "abs = (pos)|"
    exp = "d =a*((b)+ c)*11e+5+1|"
    # exp = "   d =  (  (a * ( ( 0.012 + 7E+50 ) )) +((dom)* 228)  )|"
    # "d =a*((b)+ c)*d+1|"
    # "abs = 3.5*((x+66E-5))+y34|"

    fsm = FSM(q_count, alphabet, transitions)
    fsm.show_transitions_table()
    actions = Actions()
    opz = execute(exp, fsm, actions)
    RPN_to_optimized_code(opz, ["+", "*", "="])


def execute(str, fsm, actions=None):  # Управляющее устройство автомата (проверяет входную цепочку и строит ОПЗ)
    priority = ["=", "(", "+", "*"]  # Чем выше индекс, тем выше приоритет
    stack = []
    temp_str = ""
    list_out = []
    condition = 0
    print(f'Execution of "{str}" string, starting condition q0')
    try:
        for i_elem in range(len(str)):  # Цикл по символам строки

            # Алгоритм ОПЗ
            # try:
            if ("E" in temp_str or "e" in temp_str) and (57 >= ord(temp_str[temp_str.find("e")-1]) >= 48 or 57 >= ord(temp_str[temp_str.find("E")-1]) >= 48):
                temp_str += str[i_elem]
                t_elem = i_elem + 1
                if re.match(r"\d+[Ee][-+]\d+", temp_str):
                    list_out.append(temp_str)
                    temp_str = ""
                # while str[t_elem] not in priority:
                #     temp_str += str[t_elem]
                #     t_elem += 1
                # list_out.append(temp_str)
                # temp_str = ""
            # except IndexError:
            #     pass
            elif str[i_elem] == "(":
                stack.append(str[i_elem])
            elif str[i_elem] == " ":
                pass
            elif str[i_elem] in priority:
                if temp_str:
                    list_out.append(temp_str)
                    temp_str = ""
                if len(stack) == 0 or priority.index(stack[len(stack) - 1]) < priority.index(str[i_elem]):
                    stack.append(str[i_elem])
                else:
                    while len(stack) != 0 and priority.index(stack[len(stack) - 1]) >= priority.index(str[i_elem]):
                        list_out.append(stack.pop())
                    stack.append(str[i_elem])
            elif str[i_elem] == ")":
                if temp_str:
                    list_out.append(temp_str)
                    temp_str = ""
                stack_elem = stack.pop()
                list_out.append(stack_elem)
                while stack_elem != "(":
                    stack_elem = stack.pop()
                    list_out.append(stack_elem)
                list_out.pop()
            elif str[i_elem] == "|" and str.index(str[i_elem]) == len(str) - 1:
                if temp_str:
                    list_out.append(temp_str)
            else:
                temp_str += str[i_elem]

            for j_elem in range(len(fsm.transitions[condition])):  # Цикл по строке состояния в таблице переходов
                try:
                    if fsm.transitions[condition][j_elem][0] != "err":
                        # Цикл по символу диапазона алфавита, соответсвующий существующему переходу в строке состояния
                        for k_elem in range(len(fsm.alphabet[j_elem])):
                            if fsm.alphabet[j_elem][k_elem] == str[i_elem]:
                                check_for_action(actions, len(fsm.transitions[condition][j_elem]),
                                                 fsm.transitions[condition][j_elem])
                                condition = int(fsm.transitions[condition][j_elem][0][1:])
                                raise Passed
                            elif fsm.alphabet[j_elem][k_elem] == "-" and k_elem != len(
                                    fsm.alphabet[j_elem]) - 1 and k_elem != 0:
                                if 57 >= ord(fsm.alphabet[j_elem][k_elem + 1]) >= 48 and 57 >= ord(
                                        fsm.alphabet[j_elem][k_elem - 1]) >= 48 \
                                        and ord(fsm.alphabet[j_elem][k_elem + 1]) >= ord(str[i_elem]) >= ord(
                                    fsm.alphabet[j_elem][k_elem - 1]):
                                    check_for_action(actions, len(fsm.transitions[condition][j_elem]),
                                                     fsm.transitions[condition][j_elem])
                                    condition = int(fsm.transitions[condition][j_elem][0][1:])
                                    raise Passed
                                elif 90 >= ord(fsm.alphabet[j_elem][k_elem + 1]) >= 65 and 90 >= ord(
                                        fsm.alphabet[j_elem][k_elem - 1]) >= 65 \
                                        and ord(fsm.alphabet[j_elem][k_elem + 1]) >= ord(str[i_elem]) >= ord(
                                    fsm.alphabet[j_elem][k_elem - 1]):
                                    check_for_action(actions, len(fsm.transitions[condition][j_elem]),
                                                     fsm.transitions[condition][j_elem])
                                    condition = int(fsm.transitions[condition][j_elem][0][1:])
                                    raise Passed
                                elif 122 >= ord(fsm.alphabet[j_elem][k_elem + 1]) >= 97 and 122 >= ord(
                                        fsm.alphabet[j_elem][k_elem - 1]) >= 97 \
                                        and ord(fsm.alphabet[j_elem][k_elem + 1]) >= ord(str[i_elem]) >= ord(
                                    fsm.alphabet[j_elem][k_elem - 1]):
                                    check_for_action(actions, len(fsm.transitions[condition][j_elem]),
                                                     fsm.transitions[condition][j_elem])
                                    condition = int(fsm.transitions[condition][j_elem][0][1:])
                                    raise Passed
                    if j_elem == len(fsm.transitions[condition]) - 1:
                        raise SyntaxError
                except Passed:
                    break
    except SyntaxError:  # Синтаксическая ошибка (недопустимый символ в алфавите или несоответствие таблице переходов)
        print(f"{str}\n" + " " * i_elem + "^" + "\nThe error occurred!")
        return False
    except ValueError:  # Разбор завершен:
        if i_elem == len(str) - 1 and actions.action3():  # верно
            Completed(1)
            while stack:
                list_out.append(stack.pop())
            print("Reverse Polish notation: " + " ".join(elem for elem in list_out))
            if "(" in str:
                print("Table of names: ) ( " + " ".join(elem for elem in set(list_out)))
            else:
                print("Table of names: " + " ".join(elem for elem in set(list_out)))
            return list_out
        elif not actions.action3():  # несоответсвие кол-ва скобок
            print("Wrong amount of open/close brackets!")
            return False
        elif i_elem != len(str) - 1:  # ошибка маркера конца разбора
            print(f"{str}\n" + " " * i_elem + "^" + "\nThe error occurred!")
            print("End-marker is not at the end of string!")
            return False
    # Строка закончилась, маркер конца не встречен
    print(f"{str}\n" + " " * i_elem + "^" + "\nString has no end-marker!")


def RPN_to_optimized_code(rpn, signs):  # Перевод из ОПЗ в псевдакод
    cr, cl = 0, 0
    stack = []
    for elem in rpn:
        if elem not in signs:
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
