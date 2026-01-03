####################################################################
#  subdomain.py                                                    #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Instance
from core.instance import database_instance as db

class Subdomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    domain_id = db.Column(
        db.Integer,
        db.ForeignKey('domain.id', ondelete='CASCADE')
    )

    # Permutations / Bruteforce
    type = db.Column(db.String)

    # Probing Attributes
    status = db.Column(db.String)
    timestamp = db.Column(db.String)
    response = db.Column(db.String)
    screenshot = db.Column(db.String)
    method = db.Column(db.String)
    status_code = db.Column(db.String)
    redirect = db.Column(db.String)
    host = db.Column(db.String)
    server = db.Column(db.String)
    cdn = db.Column(db.String)
    content_type = db.Column(db.String)
    content_length = db.Column(db.String)
