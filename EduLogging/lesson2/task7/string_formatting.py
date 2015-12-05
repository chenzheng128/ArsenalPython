from __future__ import print_function
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    logging.debug('this message is not formatted; value=%s %s', 'value', 'value')

    logging.debug('this message is not formatted; value=%s' , 'value' )


