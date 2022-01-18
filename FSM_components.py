class FSM:
    """Параметры класса ДКА:
    alphabet - Алфавит автомата, где разделителем является знак "|",
    q_count - Множество состояний, представленных численно от 0 (q0 или нач. сотояние) до q_count - 1

    self.transition - Функция переходов, где transitions[состояние q][диапазон алфавита][в какое состояние
    выполняется переход и цифра: если нет цифры, то внедренное действие не требуется,
    а если "1" - action1, "2" - action2, "3" - action3]. Например, q1|2 (переход в состояние 1 с внедренным действием 2)

    Маркером конца цепочки принять за сивол "|" в входной цепочке или halt в файле input.txt

    Если нету перехода из данного состояния в другое, то оставить место пустым пробелом (в начале и в конце пробел не нужен).
    Пример: "q0|2~q0~ ~q0~q0" эквивалентно состоянию перехода в таблице как q0,2; q0; err, 0; q0; q0

    Если разбор завершается верно, то переход должен произойти в "halt|3" и только в маркере конца цепочти "|", т.е.
    последний столбец в таблице состояний.

    По умолчанию каждое состояние инициализируется [['err'], ['err'], ['err']]
    """
    def __init__(self, q_count, alphabet, transitions):
        alphabet.append("|")
        self.q = q_count
        self.alphabet = alphabet
        self.transitions = [[["err"] for _ in alphabet] for _ in range(q_count)]
        self.set_transitions(transitions)

    def set_transitions(self, tr):
        for i_condition in range(len(tr)):
            for i_transition in range(len(tr[i_condition])):
                if tr[i_condition][i_transition][0] != " " and tr[i_condition][i_transition][0] != "":
                    self.transitions[i_condition][i_transition] = tr[i_condition][i_transition]

    def show_transitions_table(self):
        print(end="\t")
        for elem in self.alphabet:
            if elem == " ":
                print(f'" "{elem:5}', end="\t")
            else:
                print(f"{elem:10}", end="\t")
        print()
        for condition in self.transitions:
            print(self.transitions.index(condition), end="\t")
            for transition in condition:
                try:
                    print(f"{transition[0]},{transition[1]:5}", end="\t")
                except IndexError:
                    print(f"{transition[0]:10}", end="\t")
            print("\n")
