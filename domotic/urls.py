from django.urls import path
from.views import AttributeListView, ChartView, TemperatureChartView

urlpatterns = [
    path('', AttributeListView.as_view()),
    path('chart/<int:pk>/', ChartView.as_view(), name='chart'),
    path('chart/temperature/', TemperatureChartView.as_view(), name='temperature_chart'),
]
