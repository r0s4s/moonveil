####################################################################
#  asn.py                                                          #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Instance
from core.instance import database_instance as db

class ASN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    target_id = db.Column(
        db.Integer,
        db.ForeignKey('target.id', ondelete='CASCADE')
    )
    