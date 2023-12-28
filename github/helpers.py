from jsonpath_ng.ext import parse


def message(label, api, ui):
    return (f'Mismatch'
            f'\nAPI:\t{api}'
            f'\nUI:\t\t{ui}'
            f'\nLabel:\t{label}')
