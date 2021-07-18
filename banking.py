import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class ATM:
    PIN = 0
    card_no = 0
    log_in_success = 0
    current_balance = 0
    exit = 1

    def __init__(self, choice):
        self.choice = choice

    @staticmethod
    def create():
        PIN = ''.join([str(random.randint(0, 9)) for x in range(4)])
        card_no = '400000' + ''.join([str(random.randint(0, 9)) for x in range(9)])
        luhn_verification = 0
        count = 0
        for digit in card_no:
            digit = int(digit)
            count += 1
            if count % 2 != 0:
                digit = digit * 2
                if digit > 9:
                    digit -= 9
            luhn_verification += digit
        for checksum in range(0, 10):
            if (checksum + luhn_verification) % 10 == 0:
                card_no += str(checksum)
                break
        print('''Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}'''.format(card_no, PIN))
        ATM.PIN = str(PIN)
        ATM.card_no = str(card_no)
        cur.execute('INSERT INTO card(number, pin, balance)\n'
                    '                        VALUES(?, ?, ?)', (ATM.card_no, ATM.PIN, ATM.current_balance))
        conn.commit()

    @staticmethod
    def balance():
        print(cur.execute('''SELECT FROM card(
                                balance AS Balance)'''))

    @staticmethod
    def log_in():
        input_card_no = input('Enter your card number:')
        input_PIN = input('Enter your PIN:')
        database = cur.execute('SELECT EXISTS(SELECT 1 FROM card WHERE number = "%s" AND pin = "%s")' % (input_card_no, input_PIN))
        for row in database:
            if int(row[0]) == 0:
                print('Wrong card number or PIN!')
            elif int(row[0]) == 1:
                print('You have successfully logged in!')
                ATM.log_in_success = 1
                ATM.card_no = input_card_no
                ATM.PIN = input_PIN

    @staticmethod
    def add_income():
        income = int(input('Enter income:'))
        balance_table = cur.execute('SELECT balance FROM card WHERE number = "%s" AND pin = "%s"'% (ATM.card_no, ATM.PIN))
        count = 0
        for row in balance_table:
            count += 1
            if count == 2:
                ATM.current_balance = int(row[0])
        ATM.current_balance += income
        cur.execute('UPDATE card SET balance = "%s" WHERE number = "%s" AND pin = "%s"' % (ATM.current_balance, ATM.card_no, ATM.PIN))
        conn.commit()
        print('Income was added!')

    @staticmethod
    def transfer():
        receiver_card_no = input('Enter card number:')
        database = cur.execute('SELECT COUNT(number) FROM card WHERE number = "%s"' % receiver_card_no)
        count = 0
        number = 0
        new_balance = 0
        checksum = 0

        for digit in receiver_card_no:
            digit = int(digit)
            count += 1
            if count % 2 != 0:
                digit = digit * 2
                if digit > 9:
                    digit -= 9
            checksum += digit

        for row in database:
            check_record = row[0]
            print(check_record)

        if checksum % 10 != 0:
            print('Probably you made a mistake in the card number. Please try again!')

        elif check_record == 0:
            print('Such a card does not exist.')

        else:
            money = int(input('Enter how much money you want to transfer:'))
            sender_database = cur.execute('SELECT balance FROM card WHERE pin = "%s" AND number = "%s"' % (ATM.PIN, ATM.card_no))

            for row in sender_database:
                if money > int(row[0]):
                    print('Not enough money!')
                    break
                else:
                    sender_balance = int(row[0]) - money
                    cur.execute('UPDATE card SET balance = "%s" WHERE number = "%s"' % (sender_balance, ATM.card_no))
                    receiver_database = cur.execute('SELECT balance FROM card WHERE number = "%s"' % receiver_card_no)
                    conn.commit()
                    for second_row in receiver_database:
                        receiver_balance = int(second_row[0])
                        receiver_balance += money
                        cur.execute('UPDATE card SET balance = "%s" WHERE number = "%s"' % (receiver_balance, receiver_card_no))
                        conn.commit()
                        print('Success!')

    @staticmethod
    def close_account():
        cur.execute('DELETE FROM card WHERE number =  "%s"' % ATM.card_no)
        conn.commit()

    @staticmethod
    def log_out():
        print('You have successfully logged out!')
        ATM.log_in_success = 0

    def first_screen(self):
        if self.choice == 0:
            ATM.exit = 0
            return
        else:
            if self.choice == 1:
                self.create()
            elif self.choice == 2:
                self.log_in()

    def second_screen(self):
        if self.choice == 0:
            ATM.exit = 0
            return
        elif self.choice == 1:
            self.balance()
        elif self.choice == 2:
            self.add_income()
        elif self.choice == 3:
            self.transfer()
        elif self.choice == 4:
            self.close_account()
        elif self.choice == 5:
            self.log_out()


while True:
    if ATM.log_in_success == 0:
        button = ATM(int(input('''1. Create an account\n2. Log into account\n0. Exit''')))
        button.first_screen()
    elif ATM.log_in_success == 1:
        button = ATM(int(input('''1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit''')))
        button.second_screen()
    if ATM.exit == 0:
        break
