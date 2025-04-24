def convert_to(number, base):
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while number > 0:
        result = (digits[number % base] + result)
        number //= base
    return result


class CalcToNotation:
    def __init__(self, data, translation, printer=True):
        if not data or not isinstance(data, (list, tuple)):
            raise Exception(f'Incorrect input. {f'Was used {type(data)}.' if not isinstance(data, (list, tuple))
                            else 'Was transferred empty object.'}')
        elif isinstance(data, tuple):
            data = list((data,))
        if translation < 2 or translation > 36:
            raise Exception(f'Incorrect input. You entered translate "{translation}"')
        self.translate = translation

        self.results = []
        for i in range(len(data)):
            if data[i][1] == 10:
                result = convert_to(int(data[i][0]), self.translate)
            elif self.translate == 10:
                result = int(data[i][0], data[i][1])
            else:
                result = convert_to(int(data[i][0], data[i][1]), self.translate)
            self.results.append(result)
            if printer:
                print(f'{data[i][0]} ({data[i][1]}) = {result} ({self.translate})')

    def comparison(self):
        maximum = convert_to(max(int(self.results[i], self.translate) for i in range(len(self.results))), self.translate)
        minimum = convert_to(min(int(self.results[i], self.translate) for i in range(len(self.results))), self.translate)
        print(f'Max: {maximum} || Min: {minimum}')
        return maximum, minimum


class CalcToPathUrl:
    def __init__(self, data, protocol, server, file):
        alfa = 'АБВГДЕЖ'
        data = data.split(' ')
        server, SExtension = server.split('.')
        file, FExtension = file.split('.')
        result, alfa_result, delta_result = '', '', ''
        for j in protocol, '://', server, '.' + SExtension, '/', file, '.' + FExtension:
            for i in range(len(data)):
                if j.lower() == data[i].lower():
                    result += str(i + 1)
                    alfa_result += alfa[i]
                    delta_result += j
                    break
        print(f'Output: "{delta_result}" || Answer "{result}" or "{alfa_result}"')
