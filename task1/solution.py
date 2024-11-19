def strict(func):
    def wrapper(*args):
        # Сравниваем типы аргументов
        for arg_value, (arg_name, annotation) in zip(
            args, func.__annotations__.items()
        ):
            if arg_name != "return" and not isinstance(arg_value, annotation):
                raise TypeError(
                    f"Аргумент '{arg_name}'должен быть типа {annotation.__name__}"
                )

        result = func(*args)

        # Сравниваем тип возврата
        return_annotation = func.__annotations__.get("return")
        if return_annotation and not isinstance(result, return_annotation):
            raise TypeError(
                f"Возвращаемое должно быть типа {return_annotation.__name__}"
            )
        return result

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
