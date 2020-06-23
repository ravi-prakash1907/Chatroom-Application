import random as r


class decrypter:
    """     docstring for decrypter      """
    def __init__(self):
        self.a = "abcdefghijklmnopqrstuvwxyz#*&@$"     #len = 31
        self.b = "%wqertyuiop*asdf-ghjkl4zxcvb#nm"     #len = 31    %*#-4
        self.c = "0123456789.%-"       #len = 13
        self.d = "50@239^$7&681"       #len = 13
        self.rand = 0

    def decodeAlter(self):
        self.t = self.b[0]
        self.b = self.b[1:]
        self.b += self.t

    def decode(self, inp):
        inp = inp.lower()

        initial = -1
        check = inp[len(inp)-1]
        for i in range(10):
            if check == self.d[i]:
                check = self.c[i]
                initial = i
                break

        for i in range(initial):
            self.__decodeAlter()

        temp = ""
        for Str in range(len(inp)):
            real = inp[Str]
            if real.isalpha() or real=='%' or real=='*' or real=='#' or real=='-' or real=='4':
                for i in range(31):
                    match = self.b[i]
                    if real == match:
                        temp += str(self.a[i])
                        self.__decodeAlter()
                        break

            elif (real.isnumeric() and real!='4') or real=='@' or real=='$' or real=='&' or real=='^': # Encrypting Digits
                for i in range(13):
                    match = self.d[i]
                    if real == match:
                        temp += str(self.c[i])
                        self.__decodeAlter()
                        break

            elif real == '\n':
                temp += str('\n')

            else:
                temp += str(real)

        temp = temp[0:len(inp)-1]
        return temp

    __decodeAlter = decodeAlter

# class ends here

def mainFun(msg):
    begin = decrypter()
    return begin.decode(msg)
# ends main







##################################################



a = "abcdefghijklmnopqrstuvwxyz#*&@$"     #len = 31
b = "%wqertyuiop*asdf-ghjkl4zxcvb#nm"     #len = 31    %*#-4
c = "0123456789.%-"       #len = 13
d = "50@239^$7&681"       #len = 13

def decodeAlter():
    global b

    t = b[0]
    b = b[1:]
    b += t


def decode(inp):
    global a
    global b
    global c
    global d

    inp = inp.lower()

    initial = -1
    check = inp[len(inp)-1]
    for i in range(10):
        if check == d[i]:
            check = c[i]
            initial = i
            break

    for i in range(initial):
        decodeAlter()

    temp = ""
    for Str in range(len(inp)):
        real = inp[Str]
        if real.isalpha() or real=='%' or real=='*' or real=='#' or real=='-' or real=='4':
            for i in range(31):
                match = b[i]
                if real == match:
                    temp += str(a[i])
                    decodeAlter()
                    break

        elif (real.isnumeric() and real!='4') or real=='@' or real=='$' or real=='&' or real=='^': # Encrypting Digits
            for i in range(13):
                match = d[i]
                if real == match:
                    temp += str(c[i])
                    decodeAlter()
                    break

        elif real == '\n':
            temp += str('\n')

        else:
            temp += str(real)

    temp = temp[0:len(inp)-1]
    return temp


















#
