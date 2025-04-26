def convert_to(number, base):
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while number > 0:
        result = (digits[number % base] + result)
        number //= base
    return result


class CalcToNotation:
    def __init__(self, data, translate=10, printer=True):
        if not data or not isinstance(data, (list, tuple)):
            raise Exception(f'Incorrect input. {f'Was used {type(data)}.' if not isinstance(data, (list, tuple))
                            else 'Was transferred empty object.'}')
        elif isinstance(data, tuple):
            data = list((data,))
        if translate < 2 or translate > 36:
            raise Exception(f'Incorrect input. You entered translate "{translate}"')

        results = []
        for i in range(len(data)):
            result = convert_to(int(data[i][0], data[i][1]), translate)
            results.append(result)
            if printer:
                print(f'{data[i][0]} ({data[i][1]}) = {result} ({translate})')

        print(f'Max: {convert_to(max([int(results[i], translate) for i in range(len(results))]), translate)} |'
              f'| Min: {convert_to(min([int(results[i], translate) for i in range(len(results))]), translate)}')


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


class CalcToB:
    def __init__(self, data, action, order):
        order = list(order)
        flag, k, n = 0, 0, 0
        for i in order:
            if i == '2':
                flag = 1
            elif flag == 0:
                n += 1
            else:
                k += 1

        if action[1] == '*':
            print(f'Answer -> {int((data[1] - k * action[0]) / (data[0] + n * action[0]))}')
        elif action[1] == '/':
            print(f'Answer -> {int((data[0] + n * action[0]) / (data[1] - k * action[0]))}')
        else:
            raise Exception(f'Incorrect input action {action[1]}')