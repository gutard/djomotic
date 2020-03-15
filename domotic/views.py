from datetime import timedelta
from serial import Serial
from struct import pack

from django.views.generic import ListView, DetailView, TemplateView, RedirectView
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


class ShutterMove(RedirectView):
    DOWN = 0x00
    UP = 0x01
    TOGGLE = 0x02

    url = '/'

    def post(self, target=0x01, cmd=TOGGLE, group=True):
        CODE = 0x0092

        # Paylod
        self.mode = 0x01 if group else 0x02  # 0=bound 1=group 2=short 3=ieee
        src = 0x01
        dst = 0x01
        payload = pack('!BHBBB', self.mode, target, src, dst, cmd)

        # Length
        length = len(payload).to_bytes(2, 'big')

        # Checksum
        code = CODE.to_bytes(2, 'big')
        checksum = code[0] ^ code[1]
        checksum ^= length[0] ^ length[1]
        for byte in self.payload:
            checksum ^= byte
        checksum = bytes([checksum])

        # Raw data
        data = code + length + checksum + payload

        # Encoded data
        encoded = bytearray([0x01])
        for byte in data:
            if byte < 0x10:
                encoded.extend([0x02, byte ^ 0x10])
            else:
                encoded.append(byte)
        encoded.append(0x03)

        # Send packet
        with Serial(port='/dev/ttyS0', baudrate=115200, timeout=5) as serial:
            serial.write(bytes(encoded))

        # Redirect
        return super().post()
