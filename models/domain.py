####################################################################
#  domain.py                                                       #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Instance
from core.instance import database_instance as db

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    target_id = db.Column(
        db.Integer,
        db.ForeignKey('target.id', ondelete='CASCADE')
    )

    # Relationship
    subdomains = db.relationship(
        'Subdomain',
        backref='domain',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
