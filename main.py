import datetime
from db_interactor import DataBaseInteractor


class BudgetElement:
    obj_list = []

    @classmethod
    def create_spreadsheet(cls):
        cls.database_int = DataBaseInteractor('financial_spreadsheet.db')
        cls.database_int.create_table('fin_balance', description='TEXT', amount='INTEGER',
                                      positivity='TEXT', date='TEXT')

    def __init__(self, description: str, amount: int | float, positivity: str, date: tuple = None):

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

        self.__class__.database_int.add_data('fin_balance',
                                             description=self.description, amount=self.amount,
                                             positivity=self.positivity, date=self.date.__str__())

    def __repr__(self):
        return f'BudgetElement(amount={self.amount}, positivity={self.positivity})'

    @classmethod
    def _calculate_budget_base(cls, date_from: datetime.date, date_to: datetime.date):

        budget = 0

        for i in cls.obj_list:
            if i.positivity == '+' and date_from <= i.date <= date_to:
                budget += i.amount
            elif i.positivity == '-' and date_from <= i.date <= date_to:
                budget -= i.amount

        return budget

    @classmethod
    def calculate_budget(cls, period_from: tuple = None, period_to: tuple = None):

        if period_from is not None and period_to is not None:

            date_from = datetime.date(period_from[2], period_from[1], period_from[0])
            date_to = datetime.date(period_to[2], period_to[1], period_to[0])

        elif period_from is not None:

            date_from = datetime.date(period_from[2], period_from[1], period_from[0])
            date_to = datetime.date.today()

        elif period_to is not None:

            date_from = datetime.date(1, 1, 1)
            date_to = datetime.date(period_to[2], period_to[1], period_to[0])

        else:

            date_from = datetime.date(1, 1, 1)
            date_to = datetime.date.today()

        return cls._calculate_budget_base(date_from, date_to)


if __name__ == '__main__':
    BudgetElement.create_spreadsheet()
    water_bill = BudgetElement('water bill for last month', 500, '-', (1, 9, 2023))
    paycheck = BudgetElement('my work paycheck', 1000, '+', (2, 9, 2023))
    food = BudgetElement('food and groceries', 150, '-', (20, 9, 2023))
    fin_count = BudgetElement.calculate_budget(period_to=(10, 9, 2023))
    print(fin_count)
