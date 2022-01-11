class Actions:
    def __init__(self, count=0):
        self.count = count

    def action1(self):
        self.count += 1

    def action2(self):
        self.count -= 1

    def action3(self):
        if self.count == 0:
            return True
        else:
            return False
