import requests
from django.http import HttpResponse, JsonResponse
import pandas as pd # type: ignore
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trade
from .forms import TradeForm, UploadExcelForm

# Create your views here.
def index(request):
    trades = Trade.objects.all().order_by('-date')
    return render(request, 'journal/index.html', {"trades": trades})

def trade_list(request):
    trades = Trade.objects.all().order_by('-date')
    success_trades = trades.filter(notes__startswith='SUCCESS')
    failure_trades = trades.filter(notes__startswith='FAIL')
    try:
        percentage = (len(success_trades) / len(trades))*100
    except ZeroDivisionError:
        percentage = 0
    total_outcome = sum(trade.outcome for trade in trades)
    total_brokerage = sum(trade.brokerage_outcome for trade in trades)
    total_outcome -= total_brokerage
    return render(request, 'journal/trade_list.html', {"trades": trades,
                                                       'total_outcome': total_outcome,
                                                       'percentage':percentage})

def trade_update(request, pk):
    trade = get_object_or_404(Trade, pk=pk)
    if request.method == 'POST':
        form = TradeForm(request.POST,request.FILES, instance=trade)
        if form.is_valid():
            form.save()
            return redirect('trade_list')
    else:
        form = TradeForm(instance=trade)
    return render(request, 'journal/trade_form.html',{'form':form})

def trade_delete(request, pk):
    trade = get_object_or_404(Trade, pk=pk)
    if request.method == 'POST':
        trade.delete()
        return redirect('trade_list')
    return render(request, 'journal/trade_confirm_delete.html', {'trade': trade})
    

def add_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trade_list')
    else:
        form = TradeForm()
    return render(request, 'journal/trade_form.html', {'form': form})
        
def export_trades_to_excel(request):
     # Query all trade entries
    trades = Trade.objects.all()
      # Create a DataFrame from the queryset
    data = {
        'date': [trade.date for trade in trades],
        'trade_type': [trade.trade_type for trade in trades],
        'stock_symbol': [trade.stock_symbol for trade in trades],
        'position_size': [trade.position_size for trade in trades],
        'entry_price': [trade.entry_price for trade in trades],
        'exit_price': [trade.exit_price for trade in trades],
        'notes': [trade.notes for trade in trades],
        'trade_outcome': [trade.trade_outcome for trade in trades],
        'trade_rationale' : [trade.trade_rationale for trade in trades],
        'time' : [trade.time for trade in trades],
        'brokerage' : [trade.brokerage for trade in trades],
        'image' : [trade.image for trade in trades]
    }
    df = pd.DataFrame(data)
    
     # Create a HttpResponse object and set the appropriate headers for an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=trades.xlsx'

    # Use pandas to write the DataFrame to the response as an Excel file
    df.to_excel(response, index=False)

    return response
    
    
def upload_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)
                # Iterate over each row in the DataFrame and save it to the database
                for index, row in df.iterrows():
                    Trade.objects.create(
                        date=row['date'],
                        stock_symbol=row['stock_symbol'],
                        trade_type =row['trade_type'],
                        entry_price=row['entry_price'],
                        exit_price=row['exit_price'],
                        position_size=row['position_size'],
                        trade_rationale=row['trade_rationale'],
                        trade_outcome=['trade_outcome'],
                        notes=row['notes'],
                        time=row['time'],
                        brokerage=row['brokerage'],
                        image=row['image']
                    )
                return redirect('trade_list')
            else:
                return HttpResponse('Please upload an Excel file.')
    else:
        form = UploadExcelForm()
    return render(request, 'journal/upload_excel.html', {'form': form})

API_KEY = '4YWWHORM2BEBO65H'
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_data(request, symbol):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    # return JsonResponse(data)
    return data

def stock_data_view(request):
    symbol = request.GET.get('symbol', 'AAPL')  # Default to AAPL if no symbol is provided
    data = get_stock_data(request, symbol)
    if 'Time Series (Daily)' in data:
        stock_data = {
            'Meta Data': data['Meta Data'],
            'Time Series (Daily)': data['Time Series (Daily)']
        }
    else:
        stock_data = {'Meta Data': {}, 'Time Series (Daily)': {}}
    # print(stock_data)
    return render(request, 'journal/stock_data.html', {'stock_data': data})

def nse_stock_data(request, symbol):
    url = f'https://www.nseindia.com/api/quote-equity?symbol={symbol}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    session = requests.Session()
    session.get('https://www.nseindia.com', headers=headers)  # Initial request to set cookies
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        stock_data = response.json()
    else:
        stock_data = {}
    return stock_data
    
def nse_stock_view(request):
    symbol = request.GET.get('symbol', 'hdfcbank').upper()
    stock_data = nse_stock_data(request, symbol)
    return render(request, 'journal/nse_stock.html', {'stock_data': stock_data})