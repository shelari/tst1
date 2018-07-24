## -*- coding: utf-8 -*-

from actions import command_parser

DB = {
    "data": {},
    "transactions": []
}


if __name__ == '__main__':
    while True:
        try:
            command = raw_input(">> ")
            stop, DB, show = command_parser(command, DB)
            if show is not None:
                print show
            if stop:
                break
        except (EOFError):
            break
