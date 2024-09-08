from random import choice


class Terminal:
    def __init__(self):
        self.user_balance = {
            "RUB": 1_000_000,
            "USD": 0,
            "EUR": 0,
            "USDT": 0,
            "BTC": 0,
        }
        self.terminal_balance = {
            "RUB": 10_000,
            "USD": 1_000,
            "EUR": 1_000,
            "USDT": 1_000,
            "BTC": 1.5,
        }
        self.rates = {
            "RUB/USD": 0.011,
            "RUB/EUR": 0.01,
            "USD/EUR": 0.9,
            "USD/USDT": 1,
            "USDT/BTC": 0.000018,
        }

    def update_rates(self):
        for currency_pair in self.rates.keys():
            if self.rates[currency_pair] != "USD/USDT":
                self.rates[currency_pair] += (self.rates[currency_pair] / 100 * 5) * choice([-1, 1])

    def exchange(self, pair, amount):
        source_currency, target_currency = pair.split("/")

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
            return f"Exchanged {amount} {source_currency} to {result} {target_currency}"
        except AttributeError:
            return "Invalid currencies entered or this type of exchange cannot be handled"

    def get_balance(self, type_of_balance):
        table = self.user_balance if type_of_balance == "user" else self.terminal_balance
        result_output = ""
        for curr in table.keys():
            result_output += f"{curr}: {table[curr]}\n"
        return result_output


if __name__ == "__main__":
    pass