# Kredit va Omonatni hisoblab beradigan kalkulyator

Kredit va omonat hisoblovchi oddiy Python kutubxonasi.


## O'rnatish

```bash
pip install credit_deposit_calculator
```


# 1. Kreditni hisoblash

```python
from calculator import Calculator
from decimal import Decimal

calculator = Calculator(
    amount=Decimal("10000000"),                 # Kredit summasi
    initial_payment_percentage=Decimal("20"),   # Boshlang‘ich to‘lov (%)
    annual_interest_rate=Decimal("25"),         # Yillik foiz stavkasi
    loan_term_months=12                         # Kredit muddati (oy)
)
```

# Differensial usuli

```python
result = calculator.differential()
print(result)
```

# Annuitet usuli
```
result = calculator.annuity()
print(result)
```

# Natija
```python
{
  "options": {
    "interest": "10000000",            # Umumiy qiymat  
    "initial_payment": "2000000.00",   # Boshlang'ich to'lov
    "debt": "8000000.00",              # Asosiy qarz
    "loan": "1124243.56",              # Kredit miqdori 
    "amount": "9124243.56",            # Umumiy qarz
    "monthly_avg": "760353.63"         # Oylik o'rtacha to'lov
  },
  "payments": [
    [
      1,            # Oy
      "593686.96",  # Foiz qismi
      "166666.67",  # Asosiy qarz
      "760353.63",  # Umumit to'lov
      "7406313.04"  # Qoldiq qarz
    ],
    ...
}
```



# 2. Omonatni hisoblash
```python
from calculator import Deposit
from decimal import Decimal

deposit = Deposit(
    principal=Decimal("5000000"),        # Dastlabki pul miqdori
    annual_rate=Decimal("22"),           # Yillik foiz stavkasi
    months=6,                            # Omonat muddati (oy)
    monthly_addition=Decimal("500000")   # Har oy qo‘shiladigan miqdor
)

result = deposit.deposit_calculator()

print(result)
```

# Natija

```python
{
  "options": {
    "interest": "2421068.50",       # Umumiy foyda
    "total_amount": "18421068.50"   # Jami pul
  },
  "payments": [
    {
      "date": "24.04.2025",         # Sana
      "interest": "156164.38",      # Oylik foyda
      "total_amount": "10500000.00" # Umumiy qo'yilgan pul
    },
    ...
  ]
}
```



