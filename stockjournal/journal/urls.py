from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('add/', views.add_trade, name='add_trade'),
    path('', views.trade_list, name='trade_list'),
    path('trade_update/<int:pk>/update/', views.trade_update, name = 'trade_update'),
    path('trade_delete/<int:pk>/delete', views.trade_delete, name='trade_delete'),
    path('export_trades/', views.export_trades_to_excel, name='export_trades'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('stock_data/', views.stock_data_view, name='stock_data'),
    path('nse_stock/', views.nse_stock_view, name='nse_stock'),
]
