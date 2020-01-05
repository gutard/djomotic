from django.views.generic import ListView, DetailView

from .models import Attribute


class AttributeListView(ListView):
    model = Attribute


class ChartView(DetailView):
    template_name = 'domotic/chart.html'
    model = Attribute

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = self.object.value_set.order_by('timestamp')
        return context
