####################################################################
#  instance.py                                                     #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# SQLAlchemy Instance
database_instance = SQLAlchemy()

# Cache Instance
cache = Cache(config={'CACHE_TYPE': 'simple'})
