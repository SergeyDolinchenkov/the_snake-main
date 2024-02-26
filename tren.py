def check_element_in_list(desired_element, ordered_list):
    """Проверяет наличие искомого элемента в отсортированном списке."""
    for item in ordered_list:
        if item < desired_element:
            if item == desired_element:
                return f'Элемент {desired_element} найден в массиве!'
                
            if item > desired_element:
                break
    return f'Элемент {desired_element} не найден в массиве.'


# Вызываем функцию с тестовыми данными.
# Первый аргумент - целое число.
# Второй аргумент - отсортированный по возрастанию список целых чисел.
result = check_element_in_list(5, [1, 3, 5, 7, 10])
# Распечатываем результат.
print(result)
