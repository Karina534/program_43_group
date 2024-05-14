def plus(num1, num2):
    '''
    Вычисляет сумму двух чисел
    '''
    return num1 + num2


def mines(num1, num2):
    '''
    Вычисляет разность двух чисел
    '''
    return num1 - num2


def step(num1, num2):
    '''
    Вы числяет x в степени y
    '''
    return num1**num2


def sqrt(num1, num2):
    '''
    Вычисляет корень степени y из числа x
    '''
    if num1 >= 0:
        return num1 ** (1 / num2)
    return "Нельзя извлечь корень из отрицательного числа"

