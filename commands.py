## -*- coding: utf-8 -*-

def set_action(arguments, db):
    """
    Устанавливает значение переменной. Если значение не заданно, сохраняет в качестве него NULL
    :param arguments: список аргументов - 1 (имя переменной) или 2 (имя переменной, значение переменной)
    :param db: словарь, структура, куда нужно сохранить переменную
    :return: структура db с сохраненной переменной (ключ-значение)
    """
    db[arguments[0]] = 'NULL'
    if len(arguments) == 2:
        db[arguments[0]] = arguments[1]
    return db

def get_action(argument, db):
    """
    Возвращает значение переменной, если она сохранена, NULL, если нет
    :param argument: имя переменной
    :param db: словарь, структура с сохраненными ранее переменными
    :return: значение переменной или NULL, если переменной с таким именем не было сохранено
    """
    if db.has_key(argument):
        return db[argument]
    else:
        return 'NULL'

def unset_action(argument, db, transaction=None):
    """
    Удвляет переменную с указанным именем, если такая была сохранена
    :param argument: имя переменной
    :param db: словарь, структура с сохраненными ранее переменными
    :param transaction: транзакция. Словарь, если действие выполняется в рамках транзакции, None, если нет
    :return: структура db с удаленной переменной; транзакция с записанным действием
    """
    if db.has_key(argument):
        if transaction is None:
            del db[argument]
        else:
            transaction[argument] = 'DEL VARIABLE'

    return db, transaction

def counts_action(argument, db):
    """
    Считает количество переменных с заданным значением
    :param argument: значение переменной
    :param db: словарь, структура с сохраненными ранее переменными
    :return: количество переменных с указанным значением
    """
    counter = 0
    for key in db:
        if db[key] == argument:
            counter += 1
    return counter