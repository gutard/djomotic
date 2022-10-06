from django.apps import AppConfig
import pigpio


class DomoticConfig(AppConfig):
    name = 'domotic'

    def ready(self):
        pi = pigpio.pi()
        pi.set_mode(17, pigpio.OUTPUT)
        pi.set_mode(27, pigpio.OUTPUT)
        pi.write(27, 1)
        pi.write(17, 0)
        pi.write(17, 1)
