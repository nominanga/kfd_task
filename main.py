from random import choice
import os


class Terminal:
    def __init__(self):
        self.user_balance = {
            "RUB": 1_000_000.0,
            "USD": 0.0,
            "EUR": 0.0,
            "USDT": 0.0,
            "BTC": 0.0,
        }
        self.terminal_balance = {
            "RUB": 10_000.0,
            "USD": 1_000.0,
            "EUR": 1_000.0,
            "USDT": 1_000.0,
            "BTC": 1.5,
        }
        self.rates = {
            "RUB/USD": 0.011,
            "RUB/EUR": 0.01,
            "USD/EUR": 0.9,
            "USD/USDT": 1.0,
            "USDT/BTC": 0.000018,
        }
        self.is_successful_exchange = False

    def update_rates(self):
        for currency_pair in self.rates.keys():
            if currency_pair != "USD/USDT":
                self.rates[currency_pair] += (self.rates[currency_pair] / 100 * 5) * choice([-1, 1])

    def exchange(self, pair: str, amount: float) -> str:

        self.is_successful_exchange = False

        try:
            source_currency, target_currency = pair.split("/")
        except ValueError:
            return "Invalid currencies entered or this type of exchange cannot be handled"

        try:
            result = amount * self.rates[pair]
            if self.user_balance[source_currency] - amount < 0:
                return "Not enough funds at user balance"
            if self.terminal_balance[target_currency] - result < 0:
                return "Not enough funds at terminal balance"
            self.user_balance[source_currency] -= amount
            self.user_balance[target_currency] += result
            self.terminal_balance[source_currency] += amount
            self.terminal_balance[target_currency] -= result
            self.is_successful_exchange = True
            return f"Exchanged {amount} {source_currency} to {result} {target_currency}"
        except KeyError:
            return "Invalid currencies entered or this type of exchange cannot be handled"

    def get_balance(self, type_of_balance):
        table = self.user_balance if type_of_balance == "user" else self.terminal_balance
        result_output = ""
        for curr in table.keys():
            result_output += f"{curr}: {table[curr]}\n"
        return result_output


class ConsoleOperator:

    def __init__(self):
        self.terminal = Terminal()

    def balance(self):
        print("User balance:")
        print(self.terminal.get_balance("user"))
        print("Terminal balance:")
        print(self.terminal.get_balance("terminal"))

    def perform_exchange(self):
        print("Exchange formats")
        for pair in self.terminal.rates.keys():
            print(pair, self.terminal.rates[pair])

        to_check_balances = input("Do you want to check balances(y/n)? ")
        print()
        if to_check_balances == "y":
            self.balance()
        currency_pair = input("Enter pair in any available format: ")
        print()
        try:
            amount = float(input("Enter amount of funds you want to exchange: "))
            print()
        except ValueError:
            print("Wrong type entered in amount. Return to menu")
            return
        print(self.terminal.exchange(currency_pair, amount))
        print()

        if self.terminal.is_successful_exchange:
            self.terminal.update_rates()

    def run(self):
        while True:
            os.system("cls")
            print("""Type any of these commands\nexchange\nbalance\nexit""")
            command = input("Enter the command: ")
            command.lower()
            print()
            if command == "exchange":
                os.system("cls")
                self.perform_exchange()
            elif command == "balance":
                os.system("cls")
                self.balance()
            elif command == "exit":
                exit()
            else:
                os.system("cls")
                print("Unknown command")


if __name__ == "__main__":
    main = ConsoleOperator()
    main.run()
