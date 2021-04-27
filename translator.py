# Made by https://github.com/its5Q and https://github.com/Monika0000

import sys
import re

operations = {
                'mov': '01{ri}{rj}',# Копирование значения из регистра rj в ri
                'mvi': '00{ri}110 {b2}', # Копирование значения регистра в аккумулятор
                'add': '10000{ri}', # Прибавление значения регистра к аккумулятору
                'sub': '10100{ri}', # Вычитание значения регистра от аккумулятора
                'hlt': '01110110',  # Остановка выполнения
                'inr': '00{ri}100', # Инкремент аккумулятора
                'dcr': '00{ri}101', # Декремент аккумулятора
                'sma': '00101111',  # Инверсия значения аккумулятора

                'lda': '00111010 {b3} {b2}',  # Запись значений аккумулятора в ячейку
                'sta': '00110010 {b3} {b2}',  # Запись значений из ячейки в аккумулятор
             }

registers = {
                'a': '111', # Аккумулятор
                'b': '000',
                'c': '001',
                'd': '010',
                'e': '011',
                'h': '100',
                'l': '101',
                'm': '110'
            }

op_regex = re.compile(r'^([a-zA-Z]{2,4}) ?([a-eA-EhHlL]?[0-9a-fA-F]{0,2})?\,? ?([a-eA-EhHlL]?[0-9a-fA-F]{0,2})')

def op_to_binary(op: str):
    # Дефолтные значения аргументов
    ri = '111'
    rj = '111'
    b2 = 0
    b3 = 0

    if not op or op.startswith('#'):
        return ''

    parsed_op = op_regex.match(op)

    command = parsed_op.group(1)
    arg1    = parsed_op.group(2)
    arg2    = parsed_op.group(3)

    binary_command  = operations.get(command)
    
    if not binary_command:
        print(f'{op} not implemented')
        return ''
    
    ri = registers.get(arg1, '')     
    rj = registers.get(arg2, '')

    if not ri:
        try:
            b2 = int(arg1, 16)
        except Exception:
            pass
        
        try:
            b3 = int(arg2, 16)
        except Exception:
            pass
    elif not rj:
        try:
            b2 = int(arg2, 16)
        except Exception:
            pass

    binary_command = binary_command.replace('{ri}', ri).replace('{rj}', rj).replace('{b2}', format(b2, '08b')).replace('{b3}', format(b3, '08b'))

    return binary_command


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Invalid usage!\nUsage: python {sys.argv[0]} <input file> <output file>")
        sys.exit()
    
    input_path  = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', errors='ignore') as ifile:
        input_lines = [line.strip().lower() for line in ifile]
    
    with open(output_path, 'w', errors='ignore') as ofile:
        for line in input_lines:
            op_binary = op_to_binary(line)
            if op_binary:
                for byte in op_binary.split(' '):
                    _hex = format(int(byte, 2), '02x')
                    print(_hex, end = ' ')
                    ofile.write(_hex + ' ')
                print()
                ofile.write('\n')