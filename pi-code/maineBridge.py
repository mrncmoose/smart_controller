import logging
import logging.handlers
import argparse
#from ApiMqttBridge import GCP_Bridge
from ApiHttpBridge import HttpBridge

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_level", 
                    help="The level of log messages to log", 
                    default="INFO", 
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    parser.add_argument("--loopDelay",
                        help="The number of seconds to wait in the listening loop",
                        default="20")
    args = parser.parse_args()

    lg = logging.getLogger(__name__)
    lg.setLevel(level = args.log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    LOG_FILENAME = 'http_bridge.log'
    eventLogger = logging.getLogger('EventLogger')
    eventLogger.setLevel(level = args.log_level)
    logFormatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
    logHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000000, backupCount=2 )
    logHandler.setFormatter(logFormatter)
    
#     ch = logging.StreamHandler()
#     ch.setFormatter(formatter)
#     lg.addHandler(ch)
    lg.addHandler(logHandler)
    
    lg.info("Starting bridge...")
    myBridge = HttpBridge()
    myBridge.blogger.setLevel(level = args.log_level)
#    myBridge.blogger.addHandler(ch)
    myBridge.blogger.addHandler(logHandler)
    myBridge.run(loopDelay=float(args.loopDelay))
