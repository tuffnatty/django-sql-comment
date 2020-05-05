Django SQL COMMENT
==================

Django management command to generate SQL for applying your models' and fields' ``verbose_name`` and ``help_text`` as PostgreSQL ``COMMENT`` statements.

Quickstart
----------

Install Django SQL COMMENT::

    pip install django-sql-comment

Add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'django_sql_comment',
        ...
    )

Run ``./manage.py sqlcomment myapp`` to look at SQL generated, or ``./manage.py sqlcomment myapp | ./manage.py dbshell`` to apply it to your database.

If you're brave enough to apply the comments automatically on every migration, you can take the risk to add to your ``AppConfig``::

    from django.db.models.signals import post_migrate
    from django_sql_comment import sqlcomment_post_migrate
    ...
    class MyAppConfig(AppConfig):
        def ready(self):
            post_migrate.connect(sqlcomment_post_migrate)
