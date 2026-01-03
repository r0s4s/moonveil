####################################################################
#  file.py                                                         #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

import json, os, time

from core.database import DatabaseHandler

class FileHandler:
    def __init__(self, target):
        self.target_dir = f'data/{target}'
        self.target = target
        self.db_handler = DatabaseHandler()

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    # Domains
    def generate_domains_file(self):
        self.ensure_directory(self.target_dir)
        domains = self.db_handler.query_target_domains(
            self.target)
        domain_names = [domain.name for domain in domains]
        file_path = os.path.join(
            self.target_dir,
            'domains.txt')
        with open(file_path, 'w') as file:
            file.write('\n'.join(domain_names))
        return file_path

    # Subdomains
    def generate_subdomains_file(self):
        self.ensure_directory(self.target_dir)
        domains = self.db_handler.query_target_domains(
            self.target)
        
        all_subdomains = []
        for domain in domains:
            subdomains = self.db_handler.query_domain_subdomains(
                domain.name)
            all_subdomains.extend([
                subdomain.name for subdomain in subdomains])

        if all_subdomains:
            file_path = os.path.join(
                self.target_dir, 'subdomains.txt')
            with open(file_path, 'w') as file:
                file.write('\n'.join(all_subdomains))
            return file_path
        else:
            return None

    # Diff
    def save_list_to_file(self, data_list, file_name):
        file_path = os.path.join(self.target_dir, file_name)
        with open(file_path, 'w') as file:
            for item in data_list:
                file.write("%s\n" % item)

    def read_list_from_file(self, file_name):
        file_path = os.path.join(self.target_dir, file_name)
        try:
            with open(file_path, 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []
        
    # Probing
    def json_to_database(self, json_file):
        with open(json_file, 'r') as file:
            lines = file.readlines()

        try:
            json_objects = [json.loads(line) for line in lines]
        except json.JSONDecodeError as error:
            print(f'Error decoding JSON in file: {json_file}')
            print(f'Error details: {error}')
            print(f'Content: {lines}')
            return False

        # Instance
        db_handler = DatabaseHandler()

        # Probing
        for obj in json_objects:
            subdomain_name = obj.get('input')
            if subdomain_name:
                
                # Attributes
                status = 'Online' if not obj.get('failed') else 'Offline'
                timestamp = time.strftime('%d %b %Y, %H:%M:%S')
                read_response = lambda path: open(path, 'r').read() if path else None

                attributes = {
                    'status': status,
                    'timestamp': timestamp,
                    'response': read_response(obj.get(
                        'stored_response_path').strip()) if obj.get(
                        'stored_response_path') else None,
                    'screenshot': obj.get(
                        'screenshot_path_rel').strip() if obj.get(
                        'screenshot_path_rel') else None,
                    'method': obj.get('method').strip() if obj.get(
                        'method') else None,
                    'status_code': obj.get('status_code') if obj.get(
                        'status_code') else None,
                    'redirect': obj.get('location').strip() if obj.get(
                        'location') else None,
                    'host': obj.get('host') if obj.get(
                        'host') else None,
                    'server': obj.get('webserver').strip() if obj.get(
                        'webserver') else None,
                    'cdn': obj.get('cdn_name').strip() if obj.get(
                        'cdn_name') else None,
                    'content_type': obj.get('content_type').strip() if obj.get(
                        'content_type') else None,
                    'content_length': obj.get('content_length') if obj.get(
                        'content_length') else None
                }

                # Update
                db_handler.update_subdomain_by_name(
                    subdomain_name, **attributes
                )

        return True

    def remove(self, filename):
        file_path = os.path.join(
            self.target_dir,
            filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'File removed: {file_path}')
