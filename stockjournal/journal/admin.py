from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'stock_symbol', 'trade_type', 'entry_price', 'exit_price', 'position_size', 'trade_rationale', 'trade_outcome', 'brokerage']
    list_filter = ['date', 'stock_symbol', 'trade_type']
    search_fields = ['stock_symbol', 'trade_rationale']