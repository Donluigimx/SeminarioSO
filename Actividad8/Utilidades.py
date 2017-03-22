def calcularMitadHorizontal(size = int(), division = int(), position = int(), message = str()):
    if position < 1:
        return -1
    if division < 2:
        return -1
    if size <= division:
        return -1
    return int(((size / division)*position)/int(2) - len(message))
