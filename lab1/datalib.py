import numpy as np

class PrepareData:
    def __init__(self):
        self.max_var = 0

    def readTest(self, filename):
        self.testname = filename
        with open(filename) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()

            self.type = self.parseType(lines[0])
            self.function = self.parseFunction(lines[1])
            self.equations = self.parseEquations(lines[2:])

            self.A = self.createA()
            self.b = self.createB()
        return self.A, self.b

    def parseType(self, type):
        return type != 'min'

    def parseFunction(self, function):
        function_variables_with_coeff = function.split(' ')[2:]
        return self.parseCoeffsAndNumbers(function_variables_with_coeff)

    def parseCoeffsAndNumbers(self, line):
        parsed = {}
        for item in line:
            coeff, var_number = item.split('x')
            parsed['x' + var_number] = int(1 if not coeff else coeff)

            self.max_var = max(self.max_var, int(var_number))
        return parsed

    def parseEquations(self, equations):
        parsed = []
        for item in equations:
            pre_parsed, b, type = self.parseEquation(item)
            parsed.append(self.convertToCanonical(pre_parsed, b, type))
        return parsed

    def parseEquation(self, equation):
        equation = equation.split('=')
        type = equation[0][-1] + '='
        b = int(equation[1])

        equation = equation[0][:-2].split(' ')
        parsed = self.parseCoeffsAndNumbers(equation)

        return parsed, b, type

    def convertToCanonical(self, parsed, b, type):
        if type == '=':
            return parsed
        parsed['x' + str(self.max_var + 1)] = -1 if type == '>=' else 1
        if b < 0:
            b = -b
            for key, value in parsed:
                parsed[key] = -value

        self.max_var += 1
        return parsed, b

    def print(self):
        print("Test name: ", self.testname)
        print("We want find", 'MAX' if self.type else 'MIN')
        print("Function is ", end='')
        for i, (key, value) in enumerate(self.function.items()):
            if i > 0:
                print('+ ', end='')
            print(('' if value == 1 else str(value)) + key + ' ', end='')
        print()
        print("Equations:")
        for equ, b in self.equations:
            for i, (key, value) in enumerate(equ.items()):
                if i > 0:
                    print('+ ', end='')
                print(('' if value == 1 else str(value)) + key + ' ', end='')
            print('=', b)
        print("A", self.A)
        print("b", self.b)

    def createA(self):
        A = []
        for equation in self.equations:
            equ = []
            for i in range(1, self.max_var + 1):
                value = 0
                try:
                    value = equation[0]['x' + str(i)]
                except:
                    pass
                equ.append(value)
            A.append(equ)
        return np.array(A)

    def createB(self):
        b = []
        for item in self.equations:
            b.append(item[1])
        return np.array(b)
