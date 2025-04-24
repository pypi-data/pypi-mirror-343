from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta


class Calculator:
    """
    :amount: Kreditning umumiy qiymati
    :initial_payment_percentage: Boshlang'ich to'lov
    :annual_interest_rate: Yillik foiz stavkasi
    :loan_term_months: Kredirning davomiyligi (oylarda)
    """
    def __init__(self, amount: Decimal, initial_payment_percentage: Decimal, annual_interest_rate: Decimal, loan_term_months: int):
        self.amount = Decimal(amount)
        self.initial_payment_percentage = Decimal(initial_payment_percentage)
        self.annual_interest_rate = Decimal(annual_interest_rate)
        self.loan_term_months = loan_term_months

    def differential(self) -> dict:
        _initial_payment = self.__initial_payment()
        _debt = self.__debt()
        monthly_principal_payment = (_debt / Decimal(self.loan_term_months)).quantize(Decimal('0.01'))
        payments = {
            'options': {},
            'payments': []
        }

        total_amount_payment = Decimal('0.00')

        for month in range(self.loan_term_months):
            interest_payment = (_debt * self.annual_interest_rate / Decimal('100.0') / Decimal('12.0')).quantize(Decimal('0.01'))
            total_monthly_payment = (monthly_principal_payment + interest_payment).quantize(Decimal('0.01'))
            _debt -= monthly_principal_payment
            monthly = [
                month + 1,
                monthly_principal_payment,
                interest_payment,
                total_monthly_payment,
                _debt.quantize(Decimal('0.01'))
            ]
            payments['payments'].append(monthly)
            total_amount_payment += total_monthly_payment

        options = {
            "interest": self.amount,
            "initial_payment": _initial_payment,
            "debt": self.__debt(),
            "loan": (total_amount_payment - self.__debt()).quantize(Decimal('0.01')),
            "amount": total_amount_payment.quantize(Decimal('0.01')),
            "monthly_avg": (total_amount_payment / Decimal(self.loan_term_months)).quantize(Decimal('0.01')),
        }
        payments['options'] = options
        return payments

    def annuity(self) -> dict:
        _initial_payment = self.__initial_payment()
        _debt = self.__debt()
        fixed_monthly_payment = self.__annuity_payment(_debt)

        payments = {
            'options': {},
            'payments': []
        }
        total_amount_payment = Decimal('0.00')
        for month in range(self.loan_term_months):
            interest_payment = (_debt * self.annual_interest_rate / Decimal('100.0') / Decimal('12.0')).quantize(Decimal('0.01'))
            monthly_principal_payment = (fixed_monthly_payment - interest_payment).quantize(Decimal('0.01'))
            _debt -= monthly_principal_payment
            monthly = [
                month + 1,
                monthly_principal_payment,
                interest_payment,
                fixed_monthly_payment,
                _debt.quantize(Decimal('0.01'))
            ]
            payments['payments'].append(monthly)
            total_amount_payment += fixed_monthly_payment
        options = {
            "interest": self.amount,
            "initial_payment": _initial_payment,
            "debt": self.__debt(),
            "loan": abs((total_amount_payment - self.__debt()).quantize(Decimal('0.01'))),
            "amount": total_amount_payment.quantize(Decimal('0.01')),
            "monthly_avg": fixed_monthly_payment.quantize(Decimal('0.01')),
        }
        payments['options'] = options
        return payments

    def __initial_payment(self) -> Decimal:
        """Boshlangich to'lov"""
        return (self.amount * self.initial_payment_percentage / Decimal('100.0')).quantize(Decimal('0.01'))

    def __debt(self) -> Decimal:
        """Kredit miqdori"""
        return (self.amount - self.__initial_payment()).quantize(Decimal('0.01'))

    def __annuity_payment(self, debt: Decimal) -> Decimal:
        monthly_interest_rate = self.annual_interest_rate / Decimal('100.0') / Decimal('12.0')
        a = monthly_interest_rate * (Decimal('1.0') + monthly_interest_rate) ** self.loan_term_months
        b = ((Decimal('1.0') + monthly_interest_rate) ** self.loan_term_months) - Decimal('1.0')
        if b == 0:
            return (debt / self.loan_term_months).quantize(Decimal('0.01'))
        annuity_factor = a / b
        return (debt * annuity_factor).quantize(Decimal('0.01'))


class Deposit:
    """
    :principal: Dastlabki pul miqdori
    :annual_rate: Yillik foiz stavkasi (foizda)
    :months: Depositning davomiyligi (oylarda)
    :monthly_addition: Har oy depozitga qo'shiladin qo'shimcha miqdor 
    """

    def __init__(self, principal: Decimal, annual_rate: Decimal, months: int, monthly_addition: Decimal = Decimal('0.00')):
        self.principal = Decimal(principal)
        self.annual_rate = Decimal(annual_rate)
        self.months = months
        self.monthly_addition = Decimal(monthly_addition)
        self.start_date = datetime.now()

    def deposit_calculator(self):
        daily_rate = self.annual_rate / Decimal('100.0') / Decimal('365.0')

        principal = self.principal
        total_interest = 0
        payments = []

        for month in range(self.months):
            current_date = self.start_date + relativedelta(months=+month)
            next_month_date = current_date + relativedelta(months=+1)
            days_in_month = Decimal((next_month_date - current_date).days)

            interest = (principal * daily_rate * days_in_month).quantize(Decimal('0.01'))
            total_interest += interest
            principal += self.monthly_addition
            date = current_date.strftime("%d.%m.%Y")
            payments.append({
                'date': date,
                'interest': interest.quantize(Decimal('0.01')),
                'total_amount': principal.quantize(Decimal('0.01')) 
            })

        monthly_data = {
            "options": {
                'interest': total_interest.quantize(Decimal('0.01')),
                'total_amount': (principal + total_interest).quantize(Decimal('0.01'))
            },
            'payments': payments
        }

        return monthly_data


deposit = Deposit(
    principal=Decimal("10000000"), 
    annual_rate=Decimal("19"), 
    months=12, 
    monthly_addition=Decimal("500000")
)
print(deposit.deposit_calculator())