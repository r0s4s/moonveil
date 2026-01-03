####################################################################
#  database.py                                                     #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

# Math
from math import ceil

# SQLAlchemy
from sqlalchemy import or_, and_ # type: ignore

# Database, QueryParser
from core.instance import database_instance as db
from core.query import QueryParser

# Models
from models.target import Target
from models.domain import Domain
from models.asn import ASN
from models.range import Range
from models.subdomain import Subdomain
from models.archive import Archive

class DatabaseHandler:
    def __init__(self):
        self.query_parser = QueryParser()
    
    # Target
    def insert_target(self, name, scope, program):
        existing_target = Target.query.filter_by(
            name=name
        ).first()
        if existing_target:
            return None

        new_target = Target(
            name=name,
            scope=scope,
            program=program
        )

        db.session.add(new_target)
        try:
            db.session.commit()
            return new_target.id
        except Exception as e:
            db.session.rollback()
            return None

    def delete_target(self, target_id):
        target = Target.query.get(target_id)
        if target:
            db.session.delete(target)
            db.session.commit()
            return True
        return False

    # By 'id'
    def query_target_by_id(self, target_id):
        return Target.query.get(target_id)

    def query_target(self, name):
        return Target.query.filter(Target.name.ilike(f'%{name}%')).all()
    
    def query_targets(self):
        return Target.query.all()
    
    def is_target_exists(self, target_name):
        target = Target.query.filter_by(name=target_name).first()
        return target is not None
        
    # Domain : Bulk
    def insert_domains(self, domains, target_id):
        new_domains = [
            Domain(name=domain, target_id=target_id)
            for domain in domains
        ]

        db.session.bulk_save_objects(new_domains)
        db.session.commit()
    
    # Target -> Domain(s)
    def query_target_domains(self, target_name):
        target = Target.query.filter_by(
            name=target_name
        ).first()
        if target:
            domains = Domain.query.filter_by(
                target_id=target.id
            ).all()
            return domains
        return []

    # ASN : Bulk
    def insert_asns(self, asns, target_id):
        new_asns = [
            ASN(name=asn, target_id=target_id)
            for asn in asns
        ]

        db.session.bulk_save_objects(new_asns)
        db.session.commit()
        
    # Range : Bulk
    def insert_ranges(self, ranges, target_id):
        new_ranges = [
            Range(name=range_val, target_id=target_id)
            for range_val in ranges
        ]

        db.session.bulk_save_objects(new_ranges)
        db.session.commit()
        
    # Subdomain : Bulk
    def insert_subdomains(self, subdomains, domain_id):
        # Domain's Subdomains
        existing_subdomains = Subdomain.query.filter(
            Subdomain.name.in_(subdomains),
            Subdomain.domain_id == domain_id
        ).all()

        existing_subdomain_names = {
            subdomain.name for subdomain in existing_subdomains
        }

        new_subdomains = [
            Subdomain(name=subdomain, domain_id=domain_id)
            for subdomain in subdomains
            if subdomain not in existing_subdomain_names
        ]

        # Add and Commit
        db.session.add_all(new_subdomains)
        try:
            db.session.commit()
            subdomains_count = len(
                existing_subdomains
                ) + len(new_subdomains)
            return subdomains_count, new_subdomains
        except Exception as error:
            db.session.rollback()
            return 0, []

    def update_subdomain_by_name(self, subdomain_name, **kwargs):
        subdomain = self.query_subdomain_by_name(subdomain_name)
        if subdomain:
            for key, value in kwargs.items():
                setattr(subdomain, key, value)
            db.session.commit()
            return True
        return False
    
    # (Subdomains) Count
    def get_subdomains_count(self, target_name):
        try:
            count = Subdomain.query.join(Domain).join(Target).filter(
                Target.name == target_name
            ).count()
            return count
        except Exception as error:
            print(f'Error counting subdomains \
                  for target \'{target_name}\': {error}')
            return 0
        
    # (Type) Count
    def get_subdomains_type_count(self, target_name, subdomain_type):
        try:
            count = Subdomain.query.join(Domain).join(Target).filter(
                Target.name == target_name,
                Subdomain.type == subdomain_type
            ).count()
            return count
        except Exception as error:
            print(f'Error counting \'{type}\' \
                  for target \'{target_name}\': {error}')
            return 0
        
    # (Status) Count
    def get_status_subdomains_count(self, target_name, status):
        try:
            count = Subdomain.query.join(Domain).join(Target).filter(
                Target.name == target_name,
                Subdomain.status == status
            ).count()
            return count
        except Exception as error:
            print(f'Error counting \'{status}\' subdomains for \
                  target \'{target_name}\': {error}')
            return 0

    # By 'name'
    def query_subdomain_by_name(self, subdomain_name):
        return Subdomain.query.filter_by(name=subdomain_name).first()

    def query_subdomain(self, subdomain_name):
        return Subdomain.query.filter(
            Subdomain.name.ilike(f"%{subdomain_name}%")
        ).all()
    
    # Domain -> Subdomain(s)
    def query_domain_subdomains(self, domain_name):
        domain = Domain.query.filter_by(
            name=domain_name
        ).first()
        if domain:
            subdomains = Subdomain.query.filter_by(
                domain_id=domain.id
            ).all()
            return subdomains
        return []
    
    # By `type`
    def query_subdomains_type(self, target_name, type):
        try:
            subdomains = Subdomain.query.join(Domain).join(Target).filter(
                Target.name == target_name,
                Subdomain.type == type
            )
            return subdomains
        except Exception as error:
            print(f'Error fetching \'{type}\' \
                  for target \'{target_name}\': {error}')
            return 0
    
    # By `status`
    def query_status_subdomains(self, target_name, status):
        try:
            subdomains = Subdomain.query.join(Domain).join(Target).filter(
                Target.name == target_name,
                Subdomain.status == status
            )
            return subdomains
        except Exception as error:
            print(f'Error fetching \'{status}\' subdomains for \
                  target \'{target_name}\': {error}')
            return 0
    
    # Archive : Bulk
    def insert_archives(self, target_id, archive_names, batch_size=10000):
        try:
            inserted_count = 0
            new_archives = []

            # Batches
            for i in range(0, len(archive_names), batch_size):
                batch_names = archive_names[i:i + batch_size]

                # Check Batch
                existing_archives = Archive.query.filter_by(
                    target_id=target_id).filter(
                    Archive.name.in_(batch_names)).all()
                
                existing_archive_names = {
                    archive.name for archive in existing_archives
                }

                batch_new_archives = [
                    Archive(target_id=target_id, name=name)
                    for name in batch_names if name not in existing_archive_names
                ]

                new_archives.extend(batch_new_archives)
                inserted_count += len(batch_new_archives)

            # Bulk Insertion
            db.session.bulk_save_objects(new_archives)
            db.session.commit()
            return inserted_count, new_archives
        except Exception as error:
            print(f'Error inserting archives: {error}')
            db.session.rollback()
            return 0, []
        
    # (Archives) Count
    def get_archives_count(self, target_name):
        try:
            count = Archive.query.join(Target).filter(
                Target.name == target_name
            ).count()
            return count
        except Exception as error:
            print(f'Error retrieving archives count \
                  for target \'{target_name}\': {error}')
            return 0

    # Query Syntax
    def build_sql_query(self, parsed_query):
        # Single Statement
        if len(parsed_query) == 3:
            attribute, _, value = parsed_query
            column = getattr(Subdomain, attribute)
            return column.ilike(f'%{value}%')
        
        # Simple Boolean Operator Statement
        elif len(parsed_query) == 7 and parsed_query[3].lower() in ('and', 'or'):
            bool_operator = parsed_query[3].lower()
            attr1, _, val1, _, attr2, _, val2 = parsed_query
            column1 = getattr(Subdomain, attr1)
            column2 = getattr(Subdomain, attr2)

            if bool_operator == 'and':
                return and_(
                    column1.ilike(f'%{val1}%'), column2.ilike(f'%{val2}%'))
            elif bool_operator == 'or':
                return or_(
                    column1.ilike(f'%{val1}%'), column2.ilike(f'%{val2}%'))
        else:
            raise ValueError('Invalid Query Syntax')

    def search_subdomains(self, target_name, query_string, page=1, per_page=10):
        # Target
        target = Target.query.filter_by(name=target_name).first()
        if not target:
            return [], 0, 0

        # Domains
        domains = Domain.query.filter_by(target_id=target.id).all()
        if not domains:
            return [], 0, 0
        
        # Query Syntax
        parsed_query = self.query_parser.parse_query(query_string)
        sql_query = self.build_sql_query(parsed_query)

        conditions = [Subdomain.domain_id == domain.id for domain in domains]
        sql_query = and_(sql_query, or_(*conditions))
        
        # Results and Pages
        total_results = Subdomain.query.filter(sql_query).count()
        num_pages = ceil(total_results / per_page)
        
        # Paginated Results
        paginated_results = Subdomain.query.filter(sql_query).paginate(
            page=page, per_page=per_page, error_out=False)
        return paginated_results.items, total_results, num_pages

    def search_archives(self, target_name, query_string, page=1, per_page=10):
        archives_query = Archive.query.filter(
            Archive.target.has(name=target_name),
            Archive.name.ilike(f'%{query_string}%')
        )

        # Results and Pages
        total_results = archives_query.count()
        num_pages = ceil(total_results / per_page)

        # Paginated Results
        paginated_results = archives_query.paginate(
            page=page, per_page=per_page, error_out=False)
        return paginated_results.items, total_results, num_pages
