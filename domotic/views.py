from datetime import timedelta

from django.views.generic import ListView, DetailView, TemplateView
from django.utils.timezone import now

from .models import Attribute, Device


class AttributeListView(ListView):
    model = Attribute


class ChartView(DetailView):
    template_name = 'domotic/chart.html'
    model = Attribute

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = self.object.value_set.order_by('timestamp')
        return context


class TemperatureChartView(TemplateView):
    template_name = 'domotic/temperature_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = {
            device.name: device.attribute_set.get(name="Température").value_set.filter(timestamp__gt=now() - timedelta(days=1)).order_by('timestamp')
            for device in Device.objects.all()
        }
        return context
