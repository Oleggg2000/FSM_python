class FSM:
    """Параметры класса ДКА:
    alphabet - Алфавит автомата, где разделителем является знак "|",
    q_count - Множество состояний, представленных численно от 0 (q0 или нач. сотояние) до q_count - 1

    self.transition - Функция переходов, где transitions[состояние q][диапазон алфавита][в какое состояние
    выполняется переход и цифра: если нет цифры, то внедренное действие не требуется,
    а если "1" - action1, "2" - action2, "3" - action3]. Например, q1|2 (переход в состояние 1 с внедренным действием 2)

    Маркером конца цепочки принять за сивол "|" в входной цепочке или halt в файле input.txt

    Если нету перехода из данного состояния в другое, то оставить место пустым пробелом (в начале и в конце пробел не нужен).
    Пример: "q0|2~q0~ ~q0~q-1|3" эквивалентно состоянию перехода в таблице как
    {'_A-DF-Za-df-z': ['q0', '2'], '=': ['q0'], '+-': ['err'], '*': ['q0'], '|': ['q-1', '3']}

    Если разбор завершается верно, то переход должен произойти в "q-1|3" и только в маркере конца цепочти "|", т.е.
    последний столбец в таблице состояний.

    По умолчанию каждое состояние инициализируется {'=': 'err', '+*': 'err', '(': 'err', ')': 'err', 'eE': 'err'},
    где ключи словаря - это алфавит языка.
    """

    def __init__(self, q_count, alphabet):
        self.q = q_count
        self.alphabet = alphabet
        self.transitions = [dict(zip(self.alphabet, ["err" for _ in range(len(self.alphabet))])) for _ in range(q_count)]
        self.rpn = []  # reverse polish notation (ОПЗ)

    def execute(self, str, actions=None):
        temp_id = ""
        stack = []
        condition = 0
        if actions is not None:
            actions_dict = {
                "1": actions.action1,
                "2": actions.action2,
                "3": actions.action3,
                "4": actions.action4,
                "5": actions.action5,
                "6": actions.action6
            }
        try:
            for elem in str:
                for key in self.transitions[condition]:
                    if elem in key:
                        if actions is not None and len(self.transitions[condition][key]) > 1:
                            temp_id = actions_dict[self.transitions[condition][key][1]](elem, temp_id, self.rpn, stack)
                        # Если нету состояния для перехода, то вызовет ошибку ValueError
                        condition = int(self.transitions[condition][key][0][1:])
                        break
                if key == list(self.transitions[condition].keys())[-1] and condition != -1:
                    raise SyntaxError
            if actions.count == 0 and condition == -1:
                print(f"{str}\nExpression is an acceptable!")
                print("Reverse Polish notation: " + " ".join(elem for elem in self.rpn))
                if "(" in str:
                    print("Table of names: ) ( " + " ".join(elem for elem in set(self.rpn)))
                else:
                    print("Table of names: " + " ".join(elem for elem in set(self.rpn)))
                return True
            elif actions.count != 0:
                print("Wrong amount of open/close brackets!")
                return False
            else:
                print(f"{str}\n" + " " * (str.find(elem) + 1) + "^" + "\nThe error occurred! There's no end-marker")
                return False
        except ValueError:  # Нету перехода из данного состояния
            print(f"{str}\n" + " " * str.find(elem) + "^" + "\nThe error occurred! There's no transition from this condition")
            return False
        except SyntaxError:  # Недопустимый символ алфавита
            print(f"{str}\n" + " " * str.find(elem) + "^" + "\nThe error occurred! This simbol isn't in alphabet")
            return False

    @staticmethod
    def parse_file(path):
        with open(path) as f:
            transitions = []
            q_count = int(f.readline())
            alphabet = f.readline()[0:-1].split("|")
            alphabet.append("|")
            for line in f:
                line_list = line[0:-1].split("~")
                for i in range(len(line_list)):
                    if line_list[i] == " " or line_list[i] == "":
                        line_list[i] = "err"
                line_list = dict(zip(alphabet, [elem.split("|") for elem in line_list]))
                transitions.append(line_list)
        return q_count, alphabet, transitions

    @property
    def transitions_table(self):
        for cond in self.transitions:
            print(cond)

    @transitions_table.setter
    def transitions_table(self, tr):
        for i in range(len(self.transitions)):
            self.transitions[i] = tr[i]
