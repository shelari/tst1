## -*- coding: utf-8 -*-
import copy
from commands import set_action, get_action, unset_action, counts_action

def apply_all(transactions, db):
    """
    Применяет все изменения из существующих транзакций к переданному состоянию базы
    :param transactions: список транзакций
    :param db: словарь, база в ее текущем состоянии
    :return: база, измененная на основе транзакций
    """
    for t in transactions:
        if len(t) == 0:
            continue
        for action in t:
            key = action.keys()[0]
            if action[key] == 'DEL VARIABLE':
                del db[key]
            else:
                db[key] = action[key]
    return db

def command_parser(command, DB):
    """
    Распознает введенные пользователем команды и выполняет соответствующие действия
    :param command: команда, введенная пользователем
    :param DB: база данных с информацией о транзакциях
    :return: False, если нужно продолжать работу, True, если нужно остановить работу приложения; измененная бвзв двнных;
            результат запроса, который нужно отобразить наэкране, None, если ничего не нужно отображать
    """
    if len(DB["transactions"]) > 0:
        current_state = copy.deepcopy(DB["data"])
        current_state = apply_all(DB["transactions"], current_state)
    else:
        current_state = DB["data"]

    line = command.split(' ')

    if line[0] == 'SET' and len(line) <= 3:
        if DB["transactions"]:
            action = set_action(line[1:], {})
            DB["transactions"][-1].append(action)
        else:
            current_state = set_action(line[1:], current_state)
    if line[0] == 'GET' and len(line) <= 2:
        value = get_action(line[1], current_state)
        return False, DB, value
    if line[0] == 'UNSET' and len(line) <= 2:
        if DB["transactions"]:
            _, action = unset_action(line[1], current_state, {})
            DB["transactions"][-1].append(action)
        else:
            current_state, _ = unset_action(line[1], current_state)
    if line[0] == 'COUNTS' and len(line) <= 2:
        counter = counts_action(line[1], current_state)
        return False, DB, counter
    if line[0] == 'END':
        if DB["transactions"]:
            current_state = copy.deepcopy(DB["data"])
            current_state = apply_all(DB["transactions"], current_state)
        return True, DB, None
    if line[0] == 'BEGIN':
        DB['transactions'].append([])
    if line[0] == 'ROLLBACK':
        if len(DB['transactions']) > 0:
            DB['transactions'] = DB['transactions'][:-1]
    if line[0] == 'COMMIT':
        DB["data"] = apply_all(DB['transactions'], DB['data'])
        DB['transactions'] = []
    return False, DB, None