#gou zao ru can: self, key, fields
#stats_seen = 1, gou zao self.gauges

from statsdpy import statsd
from tests import utils

class StatsdTest(utils.TestCase):

    def test_process_gauge(self):
        statsd = StatsdServer()
        statsd.gauges = {'aa':10,'bb':20,'cc':30}
        statsd.stats_seen = 1
        key = 'aa'
        fields = {'10', 'g'}
        
        statsd.process_gauge(key,s fields)
        self.assertEqual(statsd.stats_seen, 2)
        self.assertEqual(statsd.gauges[key], fields[0])
        
    
