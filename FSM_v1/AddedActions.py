class Actions:
    def __init__(self, count=0):
        self.count = count
        self.priority = ["=", "(", "+", "*"]  # Чем выше индекс, тем выше приоритет

    # Подсчет скобок в выражении (Вместо магазина на ДМПА)
    def action1(self, elem, outstr, rpn, stack):  # Открывающая скобка
        self.count += 1
        stack.append(elem)
        return outstr

    def action2(self, elem, outstr, rpn, stack):  # Закрывающая скобка
        self.count -= 1
        if outstr:
            rpn.append(outstr)
            outstr = ""
        stack_elem = stack.pop()
        rpn.append(stack_elem)
        while stack_elem != "(":
            stack_elem = stack.pop()
            rpn.append(stack_elem)
        rpn.pop()
        return outstr

    @staticmethod
    def action3(elem, outstr, rpn, stack):  # Разбор завершен
        if outstr:
            rpn.append(outstr)
            outstr = ""
        while stack:
            rpn.append(stack.pop())
        return outstr

    @staticmethod
    def action4(elem, outstr, rpn, stack):  # Часть операнда
        outstr += elem
        return outstr

    @staticmethod
    def action5(elem, outstr, rpn, stack):  # Пробелы
        if outstr:
            rpn.append(outstr)
            outstr = ""
        return outstr

    def action6(self, elem, outstr, rpn, stack):  # Знаки операций
        if outstr:
            rpn.append(outstr)
            outstr = ""
        if len(stack) == 0 or self.priority.index(stack[len(stack) - 1]) < self.priority.index(elem):
            stack.append(elem)
        else:
            while len(stack) != 0 and self.priority.index(stack[len(stack) - 1]) >= self.priority.index(elem):
                rpn.append(stack.pop())
            stack.append(elem)
        return outstr
