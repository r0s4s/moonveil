####################################################################
#  search.py                                                       #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Math
from math import ceil

from flask import (
    abort,
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)

# Core
from core.database import DatabaseHandler

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/search')
def search_root():
    # Redirect
    return redirect(
        url_for('search.search_route')
    )

@search_blueprint.route('/search/<target_name>')
def search_route(target_name):
    # Check
    if not DatabaseHandler().is_target_exists(target_name):
        abort(404)
    
    # Available Attack Surface
    available_asm = 0
    if target_name in session and 'available_asm' in session[target_name]:
        available_asm = session[target_name]['available_asm']

    return render_template(
        'search.html',
        target_name=target_name,
        available_asm=available_asm
    )

@search_blueprint.route('/search/assets', methods=['GET'])
async def search_assets():
    # Form
    query_string = request.args.get('query_string')
    search_type = request.args.get('search_type')

    # Validation
    if not query_string:
        return jsonify({
            'error': 'Missing required field: query_string'
        }), 400
    
    # Target
    target_name = request.args.get('target_name')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400
    
    # Instance
    results = []
    db_handler = DatabaseHandler()

    # Search (`search_type`)
    total_results = 0
    if search_type == 'subdomains':
        page = int(request.args.get('page', 1))
        results, total_results, num_pages = db_handler.search_subdomains(
            target_name, query_string, page)
    elif search_type == 'archives':
        page = int(request.args.get('page', 1))
        results, total_results, num_pages = db_handler.search_archives(
            target_name, query_string, page)
    else:
        return jsonify({'error': 'Invalid search type'}), 400

    # No Results
    search_performed = True

    # Screenshot Directory
    screenshot_directory = f'content/{target_name}/screenshot/'

    # Available Attack Surface
    available_asm = 0
    if target_name in session and 'available_asm' in session[target_name]:
        available_asm = session[target_name]['available_asm']

    # Pagination
    page = int(request.args.get('page', 1))
    results_per_page = 10
    num_pages = ceil(total_results / results_per_page)

    # Dynamic Pagination
    pages_to_show = 5
    half_pages_to_show = pages_to_show // 2
    start_page = max(1, page - half_pages_to_show)
    end_page = min(num_pages, start_page + pages_to_show - 1)
    page_numbers = list(range(start_page, end_page + 1))

    return render_template(
        'search.html',
        target_name=target_name,
        query_string=query_string,
        search_type=search_type,
        results=results,
        results_count=total_results,
        search_performed=search_performed,
        available_asm=available_asm,
        screenshot_directory=screenshot_directory,
        page=page,
        num_pages=num_pages,
        page_numbers=page_numbers
    )
