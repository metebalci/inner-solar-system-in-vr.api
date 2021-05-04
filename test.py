import api
from tornado.log import enable_pretty_logging


enable_pretty_logging()


if __name__ == "__main__":

    print(api.get_positions('mercury', -44, 44))
    print(api.get_positions('venus', -112, 112))
    print(api.get_positions('earth', -182, 183))
    print(api.get_positions('moon', -15, 16))
    print(api.get_positions('mars', -343, 344))
    print(api.get_psp_positions(-60, 61, 24))

    days = 365
    print(api.get_positions('sun', -days, 1, 4))
    print(api.get_positions('mercury', -days, 1, 4))
    print(api.get_positions('venus', -days, 1, 4))
    print(api.get_positions('earth', -days, 1, 4))
    print(api.get_positions('moon', -days, 1, 4))
    print(api.get_positions('mars', -days, 1, 4))
    print(api.get_psp_positions(-days, 1, 4))
