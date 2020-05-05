from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, connections, router, transaction
from django.utils.encoding import force_text
from django.utils.text import camel_case_to_spaces


__version__ = '0.0.1'


def field_name_is_auto(field):
    return field.verbose_name == field.name.replace('_', ' ')


def model_name_is_auto(model):
    return model._meta.verbose_name == camel_case_to_spaces(model.__name__)


def sqlcomment_statements(app_config, using=DEFAULT_DB_ALIAS):
    with connections[using].cursor() as cursor:
        def out(query, arg):
            return cursor.mogrify(query, (arg,)).decode('utf-8')

        for model in app_config.get_models():
            table = model._meta.db_table
            comment = (None if model_name_is_auto(model)
                       else model._meta.verbose_name)
            yield out('COMMENT ON TABLE "{}" IS %s'.format(table),
                      comment or None)
            for f in model._meta.fields:
                strings = (('' if field_name_is_auto(f) else f.verbose_name),
                           f.help_text)
                comment = ' | '.join(map(force_text, filter(None, strings)))
                yield out('COMMENT ON COLUMN "{}"."{}" IS %s'
                          .format(table, f.column),
                          comment or None)


def sqlcomment_post_migrate(app_config, using=DEFAULT_DB_ALIAS, apps=apps,
                            **kwargs):
    app_label = app_config.label
    if not router.allow_migrate(using, app_label):
        return

    stmts = list(sqlcomment_statements(app_config, using=using))
    if stmts:
        with connections[using].cursor() as cursor:
            with transaction.atomic():
                for stmt in stmts:
                    cursor.execute(stmt)
