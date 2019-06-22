class one:
    def __init__(self, arg):
        print("one")


class two(one):         # two inherits from one
    def __init__(self):
        super().__init__(self)
        print("two")


two()
