from django.urls import path
from.views import AttributeListView, ChartView, TemperatureChartView, ShutterMove

urlpatterns = [
    path('', AttributeListView.as_view()),
    path('chart/<int:pk>/', ChartView.as_view(), name='chart'),
    path('chart/temperature/', TemperatureChartView.as_view(), name='temperature_chart'),
    path('shutter/toggle/', ShutterMove.as_view(cmd=ShutterMove.TOGGLE), name='shutter_all_toggle'),
    path('shutter/up/', ShutterMove.as_view(cmd=ShutterMove.UP), name='shutter_all_up'),
    path('shutter/down/', ShutterMove.as_view(cmd=ShutterMove.DOWN), name='shutter_all_down'),
]
