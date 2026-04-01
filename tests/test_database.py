####################################################################
#  test_database.py                                                #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import pytest
from core.app import create_app
from core.instance import database_instance as db
from core.database import DatabaseHandler

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def handler(app):
    with app.app_context():
        yield DatabaseHandler()

def test_insert_target(handler):
    target_id = handler.insert_target('yahoo', 'Open', 'HackerOne')
    assert target_id is not None

def test_duplicate_target_returns_none(handler):
    handler.insert_target('yahoo', 'Open', 'HackerOne')
    result = handler.insert_target('yahoo', 'Open', 'HackerOne')
    assert result is None

def test_query_targets_empty(handler):
    targets = handler.query_targets()
    assert targets == []

def test_insert_and_query_domains(handler):
    target_id = handler.insert_target('yahoo', 'Open', 'HackerOne')
    handler.insert_domains(['yahoo.com', 'yimg.com'], target_id)
    domains = handler.query_target_domains('yahoo')
    assert len(domains) == 2
