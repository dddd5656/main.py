def calculator(operation, num1,num2):
    if operation == '+':
        result = num1+num2
    elif operation == '-':
        result = num1-num2
    elif operation == '/':
        result = num1 / num2
    elif operation == '*':
        result = num1 * num2
    else:
        result = "Недопустимая операция"
    return result

operation = input("Введите операция (+,-,/,*): ")
num1 = float(input("Введите первое число:"))
num2 = float(input("Введите второе число:"))

result = calculator(operation,num1,num2)
print("Результат:",result)