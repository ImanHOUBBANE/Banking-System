import random
import sqlite3
import os

def print_login_into():
    print("""1.Create an account
2.Log into account
0.Exit""")


def print_login_out():
    print("""1. Balance
2.Log out
0.Exit""")

def check_card(input_card):
    res = list(str(input_card))
    last_element = res[-1]
    res.pop()
    res = [int(x) for x in res]
    res = [res[x] * 2 if (x +1)% 2 != 0 else res[x] for x in range(len(res))]
    res = [x - 9 if x >9 else x for x in res]
    res.append(int(last_element))
    somme = 0
    for i in res:
        somme += i
    if somme % 10 == 0:
        return True
    else:
        return False

class BankAccount:



    def create_account(self):

        self.account = 0
        card_number_without_check = '400000' + ''.join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 9))
        self.pin_number = '' + ''.join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 4))

        res = list(card_number_without_check)
        res = [int(x) for x in res]
        res = [res[x] * 2 if (x + 1) % 2 != 0 else res[x] for x in range(len(res))]
        res = [x - 9 if x > 9 else x for x in res]
        check = 0
        for element in res:
            check += element
        for digit_check in range(0,10):
            if (check + digit_check) % 10 == 0:
                self.card_number=card_number_without_check + str(digit_check)
        Connection = sqlite3.connect("card.s3db")
        Cursor = Connection.cursor()

        Cursor.execute(f'insert into card(pin,number) values({self.pin_number},{self.card_number});')
        Connection.commit()
        Connection.close()


def main():
    Connection = sqlite3.connect("card.s3db")
    Cursor = Connection.cursor()
    Cursor.execute(f'create table if not exists card(id integer primary key autoincrement,number text,pin text,balance integer default 0);')



    while True:
        print_login_into()
        option_client = input()

        while int(option_client) != 1 and int(option_client) != 2 and int(option_client) != 0:
            option_client = input()
        if int(option_client) == 1:
            client = BankAccount()
            client.create_account()
            print("Your card has been created")
            print("Your card number:")
            print(client.card_number)
            print("Your card PIN:")
            print(client.pin_number)
        if int(option_client) == 2:
            print("Enter your card number:")
            card_input = int(input())
            print("Enter your PIN:")
            pin_input = int(input())
            if check_card(card_input) == False or pin_input != int(client.pin_number):
                print("Wrong card number or PIN!")
            else:
                while True:
                    print("You have successfully logged in!")
                    print_login_out()
                    option_client_2 = input()
                    while int(option_client_2) != 1 and int(option_client_2) != 2 and int(option_client_2) != 0:
                        option_client = input()
                    if int(option_client_2) == 1:
                        Cursor.execute(f'select balance from card where pin={pin_input} and number={card_input};')
                        balance=Cursor.fetchall()
                        print(f"Balance: {balance[0][0]}")
                    if int(option_client_2) == 2:
                        print("You have successfully logged out!")
                        break
                    if int(option_client_2) == 0:
                        print("Bye")
                        Connection.close()
                        exit(1)

        if int(option_client) == 0:
            print("Bye")
            Connection.close()
            exit(1)

if __name__ == "__main__":
    main()