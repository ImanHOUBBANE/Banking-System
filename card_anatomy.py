import random



def print_login_into():
    print("""1.Create an account
2.Log into account
0.Exit""")


def print_login_out():
    print("""1. Balance
2.Log out
0.Exit""")



class BankAccount:

    def __init__(self):
        self.credentials=[]

    def create_account(self):

        self.account = 0
        self.card_number = '400000' + ''.join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 10))
        self.pin_number = '' + ''.join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 4))
        self.credentials.append(self.card_number)
        self.credentials.append(self.pin_number)
    def show_credentials(self):
        return self.credentials[0], self.credentials[1]
    def show_account(self):
        return self.account

def main():
    while True:
        print_login_into()
        option_client = input()

        while  int(option_client) != 1 and int(option_client) != 2 and int(option_client) != 0:
            option_client = input()
        if int(option_client) == 1:
            client = BankAccount()
            client.create_account()
            card, pin = client.show_credentials()
            print("Your card has been created")
            print("Your card number:")
            print(card)
            print("Your card PIN:")
            print(pin)
        if int(option_client) == 2:
            print("Enter your card number:")
            card_input = int(input())
            print("Enter your PIN:")
            pin_input = int(input())
            if card_input != int(card) or pin_input != int(pin):
                print("Wrong card number or PIN!")
            else:
                while True:
                    print("You have successfully logged in!")
                    print_login_out()
                    option_client_2 = input()
                    while int(option_client_2) != 1 and int(option_client_2) != 2 and int(option_client_2) != 0:
                        option_client = input()
                    if int(option_client_2) == 1:
                        print(f"Balance: {client.show_account()}")
                    if int(option_client_2) == 2:
                        print("You have successfully logged out!")
                        break
                    if int(option_client_2) == 0:
                        exit(1)
        if int(option_client) == 0:
            exit(1)

if __name__ == "__main__":
    main()
