import logging
from handler import PickleHttpHandler

log = logging.getLogger('SPAgent')
log.setLevel( logging.INFO )

log.addHandler( PickleHttpHandler( 'localhost:39', 'log', method='POST' ) )

for i in range(0,200):
    log.info( 'Man! %s %s %i', 'c=d', 12, i )