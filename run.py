####################################################################
#  run.py                                                          #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

from configparser import ConfigParser
from core.app import create_app

# Config
config = ConfigParser()
config.read('config.ini')
host = config.get('Server', 'Host')
port = config.get('Server', 'Port')
debug = config.get('Server', 'Debug')

app = create_app()

if __name__ == '__main__':
    app.run(
        host=host,
        port=port,
        debug=debug
    )
