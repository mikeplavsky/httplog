import logging
import logging.handlers

log = logging.getLogger('SPAgent')
log.setLevel( logging.INFO )

log.addHandler( logging.handlers.HTTPHandler( 'localhost:39', 'log' ) )

log.info( '5' )