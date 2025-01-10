from Lessons14 import result


def convert_temperature(celsius):
    kelvin=celsius + 273.15
    fahrenheit=celsius * 1.80 + 32.00
    return(kelvin, 5), (fahrenheit, 5)

# Пример 1
celsius1 = 36.50
result1 = convert_temperature(celsius1)
print(result)  # [309.65, 97.7]


# Пример 2
celsius2 = 122.11
result2 = convert_temperature(celsius2)
print(result2)  # [395.26, 251.8]
