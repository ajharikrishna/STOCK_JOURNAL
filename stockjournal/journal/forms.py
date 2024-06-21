from django import forms
from .models import Trade

# class TradeForm(forms.ModelForm):
#     class Meta:
#         model = Trade
#         fields = ['date', 'stock_symbol', 'trade_type', 'entry_price', 'exit_price', 'position_size', 'trade_rationale', 'notes']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = [
            'date',
            'time',  # New field
            'stock_symbol',
            'trade_type',
            'entry_price',
            'exit_price',
            'position_size',
            'trade_rationale',
            # 'trade_outcome',
            'brokerage',  # New field
            'image',  # New field
            'notes'
        ]
    


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()
    
