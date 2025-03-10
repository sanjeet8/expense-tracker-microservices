from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('rent', 'Rent'),
        ('shopping', 'Shopping'),
        ('other', 'Other'),
    ]
    
    user_id = models.IntegerField(default=1)  # Store only user_id, no ForeignKey
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - {self.amount} ({self.category})"
