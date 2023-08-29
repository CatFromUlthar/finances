import datetime
from db_interactor import DataBaseInteractor


class BudgetElement:
    obj_list = []

    def __init__(self, description: str, amount: int | float, positivity: str, date: tuple = None):

        database_int = DataBaseInteractor('financial_spreadsheet.db')

        database_int.create_table('fin_balance', description='TEXT', amount='INTEGER',
                                  positivity='TEXT', date='TEXT')

        self.description = description

        self.amount = amount

        if date is None:
            self.date = datetime.date.today()
        else:
            self.date = datetime.date(date[2], date[1], date[0])

        if positivity == '+' or positivity == '-':
            self.positivity = positivity
        else:
            raise ValueError("Only '+' (revenue) or '-' (costs) allowed")

        self.__class__.obj_list.append(self)

        database_int.add_data('fin_balance', description=self.description, amount=self.amount,
                              positivity=self.positivity, date=self.date.__str__())

    def __repr__(self):
        return f'BudgetElement(amount={self.amount}, positivity={self.positivity})'

    @classmethod
    def calculate_budget(cls):

        budget = 0

        for i in cls.obj_list:
            if i.positivity == '+':
                budget += i.amount
            else:
                budget -= i.amount

        print(f'Общий бюджет составляет {budget}')


if __name__ == '__main__':
    water_bill = BudgetElement('water bill for last month', 500, '-', (1, 9, 2023))
    paycheck = BudgetElement('my work paycheck', 1000, '+', (2, 9, 2023))
    food = BudgetElement('food and groceries', 150, '-')
    BudgetElement.calculate_budget()
