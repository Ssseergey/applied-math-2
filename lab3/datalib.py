import numpy as np

class PrepareData:
    def __init__(self):
        self.max_var = 0

    def readTest(self, filename):
        self.max_var = 0
        self.max_x = 0
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
        parsed = self.parseCoeffsAndNumbers(function_variables_with_coeff)
        for key, value in parsed.items():
            parsed[key] = int(value)
        return parsed

    def parseCoeffsAndNumbers(self, line):
        parsed = {}
        for item in line:
            coeff, var_number = item.split('x')
            if not coeff:
                parsed['x' + var_number] = 1
            elif coeff == '-':
                parsed['x' + var_number] = -1
            else:
                parsed['x' + var_number] = float(coeff)

            self.max_var = max(self.max_var, int(var_number))
        return parsed

    def parseEquations(self, equations):
        parsed = []
        pre_parsed, b, type = [], [], []
        for item in equations:
            pre_parsed_part, b_part, type_part = self.parseEquation(item)
            pre_parsed.append(pre_parsed_part)
            b.append(b_part)
            type.append(type_part)

        self.max_x = self.max_var
        for i in range(len(equations)):
            parsed.append(self.convertToCanonical(pre_parsed[i], b[i], type[i]))
        return parsed

    def parseEquation(self, equation):
        equation = equation.split('=')
        type = '=' if equation[0][-1] == ' ' else equation[0][-1] + '='
        b = int(equation[1])

        equation = equation[0][:-len(type)].split(' ')
        parsed = self.parseCoeffsAndNumbers(equation)

        return parsed, b, type

    def convertToCanonical(self, parsed, b, type):
        if type == '=':
            if b < 0:
                # print(parsed)
                b = -b
                for key, value in parsed.items():
                    parsed[key] = -value
            return parsed, b

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
        for equ in self.equations:
            for i, (key, value) in enumerate(equ[0].items()):
                if i > 0:
                    print('+ ', end='')
                print(('' if value == 1 else str(value)) + key + ' ', end='')
            print('=', equ[1])
        print("A")
        print(self.A)
        print("b")
        print(self.b)

    def createA(self):
        A = []
        for equation in self.equations:
            line = []
            for i in range(1, self.max_var + 1):
                value = 0
                try:
                    value = equation[0]['x' + str(i)]
                except:
                    pass
                line.append(value)
            A.append(line)
        line = []
        for i in range(1, self.max_var + 1):
            value = 0
            try:
                value = self.function['x' + str(i)]
            except:
                pass
            line.append(value)
        A.append(line)
        return np.array(A, dtype=np.float64)

    def createB(self):
        b = []
        for item in self.equations:
            b.append(item[1])
        b.append(0)
        return np.array(b, dtype=np.float64)
