# journal/models.py

from django.db import models

# class Trade(models.Model):
#     TRADE_TYPES = [
#         ('Buy', 'Buy'),
#         ('Sell', 'Sell'),
#     ]

#     date = models.DateField()
#     stock_symbol = models.CharField(max_length=10)
#     trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
#     entry_price = models.DecimalField(max_digits=10, decimal_places=2)
#     exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     position_size = models.IntegerField()
#     trade_rationale = models.TextField()
#     trade_outcome = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     notes = models.TextField(blank=True)

class Trade(models.Model):
    TRADE_TYPES = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
    ]

    date = models.DateField()
    time = models.TimeField()  # New time field
    stock_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    position_size = models.IntegerField()
    trade_rationale = models.TextField()
    trade_outcome = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='trade_images/', null=True, blank=True)  # New image field
    brokerage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New brokerage 
    def save(self, *args, **kwargs):
        if self.notes:
            self.notes = self.notes.upper()
        if self.exit_price and self.entry_price and self.position_size:
            if self.trade_type == 'Buy':
                self.trade_outcome = (self.exit_price - self.entry_price) * self.position_size
            else:
                self.trade_outcome = (self.entry_price - self.exit_price) * self.position_size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stock_symbol} - {self.trade_type} on {self.date}"
    
    @property
    def outcome(self):
        if self.trade_type == 'Buy':
            return (self.exit_price - self.entry_price) * self.position_size
        elif self.trade_type == 'Sell':
            return (self.entry_price - self.exit_price) * self.position_size
        return 0
    @property
    def brokerage_outcome(self):
        return self.brokerage