def decorator_name(func):
    def wrapper():
        print('До выполнения функции')
        func()
        print('После выполнения функции')

    return wrapper


@decorator_name
def my_func():
    print('OK')
