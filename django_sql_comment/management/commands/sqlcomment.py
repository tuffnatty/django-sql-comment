import sys

from django.apps import apps
from django.core.management.base import BaseCommand

from django_sql_comment import sqlcomment_statements


class Command(BaseCommand):
    help = 'Shows SQL to apply model/field comments to a PostgreSQL database'

    def add_arguments(self, parser):
        parser.add_argument('app_label')

    def handle(self, *args, **options):
        app_config = apps.get_app_config(options['app_label'])
        sys.stdout.write('BEGIN;\n')
        for stmt in sqlcomment_statements(app_config):
            sys.stdout.write(stmt + ';\n')
        sys.stdout.write('COMMIT;\n')
