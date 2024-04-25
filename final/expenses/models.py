from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    CATEGORIES = [
        ('amazon', 'Amazon'),
        ('groceries', 'Groceries'),
        ('eating_out', 'Eating Out'),
        ('school', 'School'),
        ('car', 'Car'),
        ('auto_insurance', 'Auto Insurance'),
        ('gas', 'Gas'),
        ('mortgage', 'Mortgage'),
        ('hoa', 'HOA'),
        ('utilities', 'Utilities'),
        ('house', 'House'),
        ('internet', 'Internet'),
        ('phone', 'Phone'),
        ('gym', 'Gym'),
        ('gifts', 'Gifts'),
        ('medical_health', 'Medical / Health'),
        ('needs', 'Needs'),
        ('wants', 'Wants'),
        ('gross_income', 'Gross Income'),
        ('net_income', 'Net Income'),
    ]
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount}"
