####################################################################
#  asm.py                                                          #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import asyncio, time

from configparser import ConfigParser

from flask import ( # type: ignore
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
from core.shell import AsyncShellCommand
from core.file import FileHandler

asm_blueprint = Blueprint('asm', __name__)

@asm_blueprint.route('/asm')
def asm_root():
    # Redirect
    return redirect(
        url_for('target.target_route')
    )

@asm_blueprint.route('/asm/<target_name>')
def asm_route(target_name):
    # Check
    if not DatabaseHandler().is_target_exists(target_name):
        abort(404)

    # Database, Session, FileHandler
    db_handler = DatabaseHandler()
    file_handler = FileHandler(target_name)
    target_data = session.get(target_name, {})

    # Default
    previous_subdomains_count = 0
    previous_subdomains_timestamp = '01 Jan 2024, 00:00:00'
    previous_archives_count = 0
    previous_archives_timestamp = '01 Jan 2024, 00:00:00'

    # Count
    subdomains_count = db_handler.get_subdomains_count(target_name)
    
    # (Permutations) Count
    permutations = db_handler.query_subdomains_type(
        target_name, 'Permutations')
    permutations = [permutation.name for permutation in permutations]
    permutations_count = len(permutations)

    # (Bruteforced) Count
    bruteforced = db_handler.query_subdomains_type(
        target_name, 'Bruteforce')
    bruteforced = [bruteforce.name for bruteforce in bruteforced]    
    bruteforced_count = len(bruteforced)

    # (Status) Counts
    online_subdomains = db_handler.get_status_subdomains_count(
        target_name, 'Online')
    offline_subdomains = db_handler.get_status_subdomains_count(
        target_name, 'Offline')

    # Subdomains Session
    new_subdomains = []
    subdomains_data = target_data.get('subdomains')
    if subdomains_data:
        previous_subdomains_count = subdomains_data.get(
            'subdomains_count')
        previous_subdomains_timestamp = subdomains_data.get(
            'timestamp')
        new_subdomains = file_handler.read_list_from_file(
            'new_subdomains.txt')

    # Available Attack Surface
    if subdomains_count > 0:
        online_percentage = round((online_subdomains / subdomains_count) * 100, 2)
        if target_name in session:
            session[target_name]['available_asm'] = online_percentage
            session.modified = True

    # Archives
    new_archives = []
    archives_count = db_handler.get_archives_count(target_name)

    # Archives Session
    archives_data = target_data.get('archives')
    if archives_data:
        previous_archives_count = archives_data.get(
            'archives_count')
        previous_archives_timestamp = archives_data.get(
            'timestamp')
        new_archives = file_handler.read_list_from_file(
            'new_archives.txt')

    # Timestamp
    timestamp = time.strftime('%d %b %Y, %H:%M:%S')

    return render_template(
        'asm.html',
        target_name=target_name,
        subdomains_count=subdomains_count,
        timestamp=timestamp,
        online_subdomains=online_subdomains,
        offline_subdomains=offline_subdomains,
        previous_subdomains_count=previous_subdomains_count,
        previous_subdomains_timestamp= previous_subdomains_timestamp,
        new_subdomains=new_subdomains[:100],
        archives_count=archives_count,
        previous_archives_count=previous_archives_count,
        previous_archives_timestamp=previous_archives_timestamp,
        new_archives=new_archives[:100],
        permutations=permutations,
        permutations_count=permutations_count,
        bruteforced=bruteforced,
        bruteforced_count=bruteforced_count
    )

@asm_blueprint.route('/asm/enumeration', methods=['POST'])
async def enumeration():
    # Form
    target_name = request.form.get('target_name')
    threads = request.form.get('threads')
    monitoring = request.form.get('monitoring')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400
    
    # Config
    config = ConfigParser()
    config.read('config.ini')
    resolvers = config.get('Files', 'Resolvers')
    subfinder = config.get('Commands', 'Subfinder')
    
    # FileHandler
    file_handler = FileHandler(target_name)
    domains_file = file_handler.generate_domains_file()

    # Instances
    db_handler = DatabaseHandler()
    cmd = AsyncShellCommand(
        subfinder.format(
            domains=domains_file,
            resolvers=resolvers,
            threads=threads
        ),
        timeout=1800
    )

    # Domains
    domains = db_handler.query_target_domains(target_name)

    # Command
    try:
        await cmd.run()
    except asyncio.TimeoutError:
        return jsonify({
            'error': 'Command execution timed out.'
        }), 500

    subdomains = cmd.get_output().split('\n')

    # (Subdomains) Bulk Insertion
    new_subdomains = []
    subdomains_count = 0
    for domain in domains:
        domain_subdomains = [
            subdomain for subdomain in subdomains if subdomain.endswith(
                f'.{domain.name}'
            )
        ]

        # Bulk Insertion
        inserted_count, inserted_subdomains = db_handler.insert_subdomains(
            domain_subdomains, domain.id
        )

        new_subdomains.extend(
            subdomain.name for subdomain in inserted_subdomains
        )

        # Count
        subdomains_count = db_handler.get_subdomains_count(target_name)

    # Session
    if monitoring == 'on':
        # Diff
        file_handler.save_list_to_file(
            new_subdomains, 'new_subdomains.txt')

        timestamp = time.strftime('%d %b %Y, %H:%M:%S')
        new_data = {
            'subdomains_count': subdomains_count,
            'timestamp': timestamp
        }

        if target_name not in session:
            session[target_name] = {}
        session[target_name]['subdomains'] = new_data
        session.modified = True

    # Clean
    file_handler.remove('domains.txt')
    return jsonify({
        'message': 'Enumeration completed successfully.'
    })

@asm_blueprint.route('/asm/archives', methods=['POST'])
async def archives():
    # Form
    target_name = request.form.get('target_name')
    monitoring = request.form.get('monitoring')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400
    
    # Config
    config = ConfigParser()
    config.read('config.ini')
    waybackurls = config.get('Commands', 'Waybackurls')
    
    # FileHandler
    file_handler = FileHandler(target_name)
    domains_file = file_handler.generate_domains_file()

    # Instances
    db_handler = DatabaseHandler()
    cmd = AsyncShellCommand(
        waybackurls.format(
            domains=domains_file
        ),
        # timeout=1800
        timeout=3600
    )

    # Target
    target = db_handler.query_target(target_name)[0]

    # Command
    try:
        await cmd.run()
    except asyncio.TimeoutError:
        return jsonify({
            'error': 'Command execution timed out.'
        }), 500

    archives = cmd.get_output().split('\n')
    
    # (Archives) Bulk Insertion
    archives_count, new_archives = db_handler.insert_archives(
        target.id,
        archives
    )

    # Session
    if monitoring == 'on':
        # Diff
        file_handler.save_list_to_file(
            [archive.name for archive in new_archives],
            'new_archives.txt'
        )

        timestamp = time.strftime('%d %b %Y, %H:%M:%S')
        new_data = {
            'archives_count': archives_count,
            'timestamp': timestamp
        }

        if target_name not in session:
            session[target_name] = {}
        session[target_name]['archives'] = new_data
        session.modified = True

    # Clean
    file_handler.remove('domains.txt')
    return jsonify({
        'message': 'Archiving completed successfully.'
    })

@asm_blueprint.route('/asm/permutations', methods=['POST'])
async def permutations():
    # Form
    target_name = request.form.get('target_name')
    limit = request.form.get('limit')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400

    # Config
    config = ConfigParser()
    config.read('config.ini')
    alterx = config.get('Commands', 'Alterx')
    
    # FileHandler
    file_handler = FileHandler(target_name)
    domains_file = file_handler.generate_domains_file()

    # Validation
    if domains_file is None:
        return jsonify({
            'error': '\'domains.txt\' is empty or no \
                domains are available for permutations.'
        }), 400

    # Instances
    db_handler = DatabaseHandler()
    cmd = AsyncShellCommand(
        alterx.format(
            domains=domains_file,
            limit=limit
        ),
        timeout=1800
    )

    # Domains
    domains = db_handler.query_target_domains(target_name)

    # Command
    try:
        await cmd.run()
    except asyncio.TimeoutError:
        return jsonify({
            'error': 'Command execution timed out.'
        }), 500
    
    permutations = cmd.get_output().split('\n')

    # (Permutations) Bulk Insertion
    for domain in domains:
        # Be careful with the solution below, replacing f'.{domain.name}'
        domain_name = domain.name.split('.')[-2] + '.' + domain.name.split('.')[-1]
        domain_permutations = [
            permutation for permutation in permutations if permutation.endswith(
                f'.{domain_name}'
            )
        ]

        # Bulk Insertion
        _, inserted_permutations = db_handler.insert_subdomains(
            domain_permutations, domain.id
        )

        # Type = Permutations
        for subdomain in inserted_permutations:
            db_handler.update_subdomain_by_name(
                subdomain.name,
                type='Permutations'
            )

    # Clean
    file_handler.remove('domains.txt')
    return jsonify({
        'message': 'Permutations generated successfully.'
    })

@asm_blueprint.route('/asm/bruteforce', methods=['POST'])
async def bruteforce():
    # Form
    target_name = request.form.get('target_name')
    threads = request.form.get('threads')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400

    # Config
    config = ConfigParser()
    config.read('config.ini')
    resolvers = config.get('Files', 'Resolvers')
    wordlist = config.get('Files', 'Wordlist')
    shuffledns = config.get('Commands', 'Shuffledns')
    
    # FileHandler
    # file_handler = FileHandler(target_name)
    # domains_file = file_handler.generate_domains_file()

    # DatabaseHandler
    db_handler = DatabaseHandler()
    domains = db_handler.query_target_domains(target_name)

    for domain in domains :

        # Instances
        # db_handler = DatabaseHandler()
        cmd = AsyncShellCommand(
            shuffledns.format(
                # domains=domains_file,
                domain=domain.name,
                resolvers=resolvers,
                wordlist=wordlist,
                threads=threads
            ),
            timeout=3600
        )

        # Domains
        # domains = db_handler.query_target_domains(target_name)

        # Command
        try:
            await cmd.run()
        except asyncio.TimeoutError:
            return jsonify({
                'error': 'Command execution timed out.'
            }), 500
        
        subdomains = cmd.get_output().split('\n')

        # (Bruteforce) Bulk Insertion
        # for domain in domains:
        # Be careful with the solution below, replacing f'.{domain.name}'
        domain_name = domain.name.split('.')[-2] + '.' + domain.name.split('.')[-1]
        domain_subdomains = [
            subdomain for subdomain in subdomains if subdomain.endswith(
                f'.{domain_name}'
            )
        ]

        # Bulk Insertion
        _, bruteforced_subdomains = db_handler.insert_subdomains(
            domain_subdomains, domain.id
        )

        # Type = Bruteforce
        for subdomain in bruteforced_subdomains:
            db_handler.update_subdomain_by_name(
                subdomain.name,
                type='Bruteforce'
            )
    
    # Clean
    # file_handler.remove('domains.txt')
    return jsonify({
        'message': 'Subdomains resolved successfully.'
    })

@asm_blueprint.route('/asm/probing', methods=['POST'])
async def probing():
    # Form
    target_name = request.form.get('target_name')
    threads = request.form.get('threads')

    # Validation
    if not target_name:
        return jsonify({
            'error': 'Missing required field: target_name'
        }), 400

    # Config
    config = ConfigParser()
    config.read('config.ini')
    httpx = config.get('Commands', 'Httpx')
    
    # FileHandler
    file_handler = FileHandler(target_name)
    subdomains_file = file_handler.generate_subdomains_file()
    output_file = f'data/{target_name}/probed.jsonl'
    content_path = f'static/content/{target_name}/'

    # Instances
    cmd = AsyncShellCommand(
        httpx.format(
            subdomains=subdomains_file,
            output_file=output_file,
            threads=threads,
            screenshots_path=content_path
        ),
        timeout=1800
    )

    # Command
    try:
        await cmd.run()
    except asyncio.TimeoutError:
        return jsonify({
            'error': 'Command execution timed out.'
        }), 500
    
    file_handler.json_to_database(output_file)
    
    # Clean
    file_handler.remove('probed.jsonl')
    file_handler.remove('subdomains.txt')
    return jsonify({
        'message': 'Subdomains probed successfully.'
    })
