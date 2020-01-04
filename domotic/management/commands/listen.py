from datetime import datetime
from serial import Serial
from struct import unpack

from django.core.management.base import BaseCommand

from ...models import Device, Attribute, Value


class Command(BaseCommand):
    def receive(self):
        packet = bytearray()
        while not packet or packet[-1] != 0x03:
            byte = self.serial.read()
            packet.extend(byte)
        if self.verbosity >= 2:
            self.stdout.write(f"Receive packet 0x{packet.hex()}")
        assert packet[0] == 0x01
        assert packet[-1] == 0x03
        data = bytearray()
        alt = False
        for byte in packet[1:-1]:
            if byte == 0x02:
                alt = True
            elif alt:
                data.append(byte ^ 0x10)
                alt = False
            else:
                data.append(byte)
        payload_length = len(data) - 6
        code, length, checksum, payload, lqi = unpack(f'!HHB{payload_length}sB', data)
        assert length == payload_length + 1  # payload + LQI
        if code != 0x8102:  # Attribute report
            return
        sqn, address, endpoint, cluster, number, type, size = unpack('!BHBHHHH', payload[:12])
        if type == 0x0029:  # INT16
            assert size == 0x0002
            value = unpack('!h', self.data)[0]
        elif type == 0x0021:  # UINT16
            assert size == 0x0002
            value = unpack('!H', self.data)[0]
        else:
            return
        device = Device.objects.get_or_create(
            address=f'{address:04x}',
            defaults={'name': f'{address:04x}'}
        )
        attribute = Attribute.objects.get_or_create(
            device=device,
            endpoint=f'{endpoint:02x}',
            cluster=f'{cluster:04x}',
            number=f'{number:04x}'
        )
        timestamp = datetime.utcnow()
        Value.objects.create(
            attribute=attribute,
            timestamp=timestamp,
            value=value
        )
        if self.verbosity >= 1:
            self.stdout.write(f"Store value {value} for device {device} at {timestamp.isoformat()}")

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        self.serial = Serial(port='/dev/ttyS0', baudrate=115200)
        while True:
            self.receive()
