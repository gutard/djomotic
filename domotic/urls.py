from django.urls import path
from.views import AttributeListView, ChartView

urlpatterns = [
    path('', AttributeListView.as_view()),
    path('chart/<int:pk>/', ChartView.as_view(), name='chart'),
]
