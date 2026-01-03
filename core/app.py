####################################################################
#  app.py                                                          #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import os, subprocess

from configparser import ConfigParser

from flask import ( # type: ignore
    Flask,
    redirect,
    url_for
)

# Instances
from core.instance import database_instance as db
from core.instance import cache

# Models
from models.target import Target
from models.asn import ASN
from models.domain import Domain
from models.range import Range
from models.subdomain import Subdomain
from models.archive import Archive

def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )

    # Config
    config = ConfigParser()
    config.read('config.ini')

    # Database Get
    container_db_path = os.environ.get('CONTAINER_DATABASE_PATH', '/moonveil/data/moonveil.db')
    
    # Update the database URI in the config.ini file
    config.set('Database', 'DatabaseURI', f'sqlite:///{container_db_path}')
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
    
    # Database
    db_uri = config.get('Database', 'DatabaseURI')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Session
    secret_key = config.get('Security', 'SecretKey')
    app.secret_key = secret_key

    # Extensions
    db.init_app(app)
    cache.init_app(app)

    # If Database does not exist
    db_path = './data/moonveil.db'
    if not os.path.exists(db_path):
        with app.app_context():
            db.drop_all()
            db.create_all()

    # Blueprints
    from routes.target import target_blueprint
    from routes.asm import asm_blueprint
    from routes.search import search_blueprint
    app.register_blueprint(target_blueprint)
    app.register_blueprint(asm_blueprint)
    app.register_blueprint(search_blueprint)

    # Root
    @app.route('/')
    def root():
        return redirect(
            url_for('target.target_route')
        )
    
    # Database Command
    @app.cli.command('init-db')
    def init_database():
        with app.app_context():
            db.drop_all()
            db.create_all()

    # Update Tools
    @app.cli.command('update-tools')
    def update_tools():
        tools = ['subfinder', 'alterx', 'dnsx', 'httpx']
        for tool in tools:
            try:
                print(f'Updating {tool}...')
                subprocess.run([tool, '--update'], check=True)
                print(f'{tool} updated successfully.')
            except subprocess.CalledProcessError as error:
                print(f'Error updating {tool}: {error}')

    return app
