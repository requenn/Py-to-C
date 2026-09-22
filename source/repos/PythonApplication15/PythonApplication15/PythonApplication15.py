#Открываем исходный файл и заранее читаем первый символ
f = open("input.py", "r", encoding="utf-8")
ch = f.read(1)

def get_token():
    global ch, f

    #Пропускаем все пробелы,табуляции,переходы на новую строку
    while ch != "" and ch.isspace():
        ch = f.read(1)

    #Если файл закончился, возвращаем заверщшение
    if ch == "":
        return "End"

    #Обработка переменной:имя должно начинаться с буквы или '_' и состоять из букв, цифр и '_'
    if ch.isalpha() or ch == "_":
        name = ""
        while ch != "" and (ch.isalnum() or ch == "_"):
            name += ch
            ch = f.read(1)
        return "Id " + name

    #Обработка чисел:целые,отрицательные и с дробной частью
    if ch.isdigit() or ch == "-":
        num = ""
        #Обработка минуса при числе
        if ch == "-":
            num += ch
            ch = f.read(1)
        # Собираем все цифры целой части
        while ch != "" and ch.isdigit():
            num += ch
            ch = f.read(1)
        # Если встретили точку,собираем дробную часть
        if ch == ".":
            num += ch
            ch = f.read(1)
            while ch != "" and ch.isdigit():
                num += ch
                ch = f.read(1)
        return "Num " + num

    #Обработка оператора присваивания
    if ch == "=":
        ch = f.read(1)
        return "Assign"

# Основной цикл:считываем токены по одному и выводим их построчно,пока не дойдем до конца файла
while True:
    token = get_token()
    print(token)
    if token == "End":
        break

# Закрываем файл
f.close()