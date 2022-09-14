import random
import sqlite3

def print_login_into():
    print("""1. Create an account
2. Log into account
0. Exit""")


def print_login_out():
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out 
0. Exit""")

def check_card(input_card):
    res = list(str(input_card))
    last_element = res[-1]
    res.pop()
    res = [int(x) for x in res]
    res = [res[x] * 2 if (x + 1) % 2 != 0 else res[x] for x in range(len(res))]
    res = [x - 9 if x > 9 else x for x in res]
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
        for digit_check in range(0, 10):
            if (check + digit_check) % 10 == 0:
                self.card_number = card_number_without_check+str(digit_check)
        Connection = sqlite3.connect("card.s3db")
        Cursor = Connection.cursor()
        Cursor.execute(f'insert into card(pin,number) values({self.pin_number},{self.card_number});')
        Connection.commit()
        Connection.close()


def main():
    Connection = sqlite3.connect("card.s3db")
    Cursor = Connection.cursor()
    Cursor.execute(f'create table if not exists card(id integer primary key autoincrement, number text, pin text, balance integer default 0);')
    Connection.commit()

    while True:
        print_login_into()
        option_client = input()
        good_option = False
        while good_option == False:
            try:
                int(option_client)
            except Exception:
                print("Choose one option from these suggestions: ")
                print_login_into()
                option_client = input()
            else:
                good_option = True

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
            Cursor = Connection.cursor()
            Cursor.execute(f"select pin ,number  from card")
            Connection.commit()
            tuple_pin_number = Cursor.fetchall()
            if (check_card(card_input) == False) or ((str(pin_input),str(card_input)) not in tuple_pin_number):
                print("Wrong card number or PIN!")
            else:
                print("You have successfully logged in!")
                while True:
                    print_login_out()
                    option_client_2 = input()
                    good_option_2 = False
                    while good_option_2 == False:
                        try:
                            int(option_client_2)
                        except Exception:
                            print("Choose one option from these suggestions: ")
                            print_login_out()
                            option_client_2 = input()
                        else:
                            good_option_2 = True
                    if int(option_client_2) == 1:
                        Cursor.execute(f'select balance from card where pin = {pin_input} and number = {card_input};')
                        balance = Cursor.fetchall()
                        Connection.commit()
                        print(f"Balance: {balance[0][0]}")

                    if int(option_client_2) == 2:
                        print("Enter income:")
                        income = int(input())
                        Cursor.execute(f'select balance,id from card where pin = {pin_input} and number = {card_input};')
                        balance_identifier = Cursor.fetchall()
                        Connection.commit()
                        Cursor.execute(f'update card set balance = {balance_identifier[0][0] + income} where id = {balance_identifier[0][1]}')
                        Connection.commit()
                        print("Income was added!")
                    if int(option_client_2) == 3:
                        print()
                        print("Transfer")
                        print("Enter card number:")
                        card_transfer = str(input())
                        Cursor.execute(f"select number from card where number = {card_transfer}")
                        Connection.commit()
                        card = len(Cursor.fetchall())
                        if card_transfer == str(card_input):
                            print("You can't transfer money to the same account!")
                        elif check_card(card_transfer) == False:
                            print("Probably you made a mistake in the card number. Please try again!")
                        elif card == 0:
                                print("Such a card does not exist.")
                        elif card != 0:
                            print("Enter how much money you want to transfer:")
                            money_tranfer = int(input())
                            Cursor.execute(f'select balance,id from card where pin = {pin_input} and number = {card_input};')
                            balance1 = Cursor.fetchall()
                            Connection.commit()
                            if (money_tranfer > balance1[0][0]) or (money_tranfer == 0):
                                print("Not enough money!")
                            else:
                                Cursor.execute(f"select balance,id from card where number={card_transfer}")
                                balance2 = Cursor.fetchall()
                                Connection.commit()
                                Cursor.execute(f'update card set balance = {balance2[0][0]+money_tranfer} where id = {balance2[0][1]}')
                                Cursor.execute(f'update card set balance = {balance1[0][0]-money_tranfer} where id = {balance1[0][1]}')
                                Connection.commit()
                                print("Success!")

                    if int(option_client_2) == 4:
                        Cursor.execute(f"select id from card where number={card_input}")
                        Connection.commit()
                        identifier = Cursor.fetchall()
                        Cursor.execute(f"delete from card where id={identifier[0][0]}")
                        Connection.commit()
                        print("The account has been closed!")
                        break
                    if int(option_client_2) == 5:
                        print("You have successfully logged out!")
                        break
                    if int(option_client_2) == 0:
                        print("Bye!")
                        Connection.close()
                        exit(1)

        if int(option_client) == 0:
            print("Bye!")
            Connection.close()
            exit(1)

if __name__ == "__main__":
    main()