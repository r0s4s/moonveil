####################################################################
#  target.py                                                       #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Instance
from core.instance import database_instance as db

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    scope = db.Column(db.String)
    program = db.Column(db.String)

    # Relationships
    asns = db.relationship(
        'ASN',
        backref='target',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    domains = db.relationship(
        'Domain',
        backref='target',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    ranges = db.relationship(
        'Range',
        backref='target',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    archives = db.relationship(
        'Archive',
        backref='target',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
