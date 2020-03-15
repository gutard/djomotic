from django.urls import path
from.views import AttributeListView, ChartView, TemperatureChartView, ShutterMove

urlpatterns = [
    path('', AttributeListView.as_view()),
    path('chart/<int:pk>/', ChartView.as_view(), name='chart'),
    path('chart/temperature/', TemperatureChartView.as_view(), name='temperature_chart'),
    path('shutter/toggle/', ShutterMove.as_view(), name='shutter_all_toggle'),
]
