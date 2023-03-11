from firefox import FireFox
import json


def main():
    ffox = FireFox()
    loginJson:json = ffox.loginJson()
    for login in loginJson['logins']:
        print(login['hostname'])


if __name__ == '__main__':
    main()