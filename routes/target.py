####################################################################
#  target.py                                                       #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import os, shutil

from flask import ( # type: ignore
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session
)

from core.database import DatabaseHandler

target_blueprint = Blueprint('target', __name__)

@target_blueprint.route('/target')
def target_route():
    # Targets
    db_handler = DatabaseHandler()
    targets = db_handler.query_targets()
    return render_template('target.html', targets=targets)

@target_blueprint.route('/target/new', methods=['POST'])
def new_target():
    # Form
    name = request.form.get('name')
    scope = request.form.get('scope') or None
    program = request.form.get('program') or None
    asns = [
        asn.strip() for asn in request.form.get(
            'asns').split('\n')
    ] if request.form.get('asns') else None
    domains = [
        domain.strip() for domain in request.form.get(
            'domains').split('\n')
    ]
    ranges = [
        range.strip() for range in request.form.get(
            'ranges').split('\n')
    ] if request.form.get('ranges') else None

    # Validation
    if not name or not domains:
        return jsonify({
            'error': 'Missing required fields: name and domains'
        }), 400
    
    # Target Directory
    target_dir = os.path.join('data', name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Target Content
    content_dir = os.path.join('static', 'content', name)
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)

    # Database Operations
    db_handler = DatabaseHandler()
    target_id = db_handler.insert_target(name, scope, program)
    if target_id is None:
        return jsonify({
            'error': 'Target already exists or failed to create'
        }), 400

    # Inserting : Bulk
    if domains:
        db_handler.insert_domains(
            domains,
            target_id
        )
    if asns:
        db_handler.insert_asns(
            asns,
            target_id
        )
    if ranges:
        db_handler.insert_ranges(
            ranges,
            target_id
        )
    return redirect('/target')

@target_blueprint.route('/target/delete/<int:target_id>', methods=['POST'])
def delete_target(target_id):
    db_handler = DatabaseHandler()

    # Session
    target = db_handler.query_target_by_id(target_id)
    if target.name in session:
        session.pop(target.name)

    success = db_handler.delete_target(target_id)
    if success:
        # Target Directory
        target_dir = os.path.join('data', target.name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        # Target Content
        content_dir = os.path.join('static', 'content', target.name)
        if os.path.exists(content_dir):
            shutil.rmtree(content_dir)
        print(f'Target successfully deleted: {success}')
    else:
        print(f'Error deleting target: {success}')
    return redirect('/target')
