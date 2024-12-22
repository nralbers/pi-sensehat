from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from sense_hat import SenseHat
from prometheus_client.registry import Collector



class CustomCollector(Collector):
    def __init__(self):
        self.sense = SenseHat()

    def collect(self):
        temperature = GaugeMetricFamily('sense_hat_temperature','Sense hat temperature in °C', labels=['sensor'], unit='celsius')
        temperature.add_metric(['humidity'],value=self.sense.get_temperature_from_humidity())
        temperature.add_metric(['pressure'], value=self.sense.get_temperature_from_pressure())
        yield temperature
        pressure = GaugeMetricFamily('sense_hat_pressure', 'Sense Hat pressure in mb', value=self.sense.get_pressure(), unit='mbar')
        yield pressure
        humidity  = GaugeMetricFamily('sense_hat_relative_humidity', 'Sense Hat Relative Humidity in %', value=self.sense.get_humidity(), unit='percent')
        yield humidity
        orientation_degrees = GaugeMetricFamily('sense_hat_orientation', 'Sense Hat orientation in degrees',labels=['axis'], unit='degrees')
        orientation_radians = GaugeMetricFamily('sense_hat_orientation', 'Sense Hat orientation in Radians',labels=['axis'], unit='radians' )
        for axis in ['pitch', 'roll', 'yaw']: 
            orientation_degrees.add_metric([axis], value=self.sense.get_orientation_degrees()[axis])
            yield orientation_degrees
            orientation_radians.add_metric([axis], value=self.sense.get_orientation_radians()[axis])
            yield orientation_radians
            
        





REGISTRY.register(CustomCollector())