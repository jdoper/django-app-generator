# -*- coding: utf-8 -*-
import shutil
import re

from django.core.management.base import BaseCommand, CommandError

from app_generator.generate_content import *
from app_generator.generate_files import *


# Geradores de arquivos
def create_python_file(app_name, name_file, fields):
    template = get_content_python(app_name, name_file, fields)
    file_path = "%s/" % app_name
    name_file = "%s.py" % name_file
    create_file(file_path, name_file, template)


def create_template_file(app_name, name_file, fields):
    template = get_content_template(app_name, name_file, fields)
    file_path = "%s/templates/%s/" % (app_name, app_name)
    name_file = "%s.html" % name_file
    create_file(file_path, name_file, template)


# Geradores de conteudos
def get_content_python(app_name, name_file, fields):
    if name_file == 'views':
        return get_content_views(app_name)
    elif name_file == 'models':
        return get_content_models(app_name, fields)
    elif name_file == 'forms':
        return get_content_forms(app_name, fields)
    elif name_file == 'urls':
        return get_content_urls(app_name)
    elif name_file == 'admin':
        return get_content_admin(app_name)


def get_content_template(app_name, name_file, fields):
    if name_file == 'base':
        return get_content_base()
    elif name_file == 'new':
        return get_content_new(app_name)
    elif name_file == 'edit':
        return get_content_edit(app_name)
    elif name_file == 'show':
        return get_content_show(app_name, fields)
    elif name_file == 'list':
        return get_content_list(app_name, fields)


# Verificadores
def check_args_errors(app_name, fields):
    pattern_app_name = re.compile("^[a-z_]+")
    pattern_field = re.compile("^[a-z_]+:[a-z]+")

    if not app_name or not isinstance(app_name[0], str) or not bool(pattern_app_name.match(app_name[0])):
        raise CommandError(u'verifique o nome do seu app, ele deve conter apenas letras e underlines')
    elif not fields:
        raise CommandError(u'não foram definidos campos para seu app')

    for field in fields:
        if not bool(pattern_field.match(field)):
            raise CommandError(u'"%s" não está no formato name_field:type_field' % field)


def check_existing_app(app_name):
    path = "%s/" % app_name

    if os.path.exists(path):
        decision = raw_input("Existe outro app com o mesmo nome, deseja exclui-lo? (S/n) ")

        while decision not in ('S', 's', 'N', 'n'):
            decision = raw_input("Valor inválido, escolha (S/n) ")

        if decision in ('N', 'n'):
            raise CommandError(u'outro app no sistema possui o mesmo nome')
        else:
            shutil.rmtree(path)


# Processadores
def process_fields(fields):
    processed_fields, check = [], []

    for field in fields:
        field = field.split(':')

        if field[0] in fields:
            raise CommandError(u'o campo %s foi definido mais de uma vez' % field[0])
        else:
            processed_fields.append(field)
            check.append(field[0])

    return processed_fields


def config_app(app_name, fields):
    create_app(app_name)
    create_folder(app_name, "templates")
    create_folder(app_name, "templates/%s" % app_name)

    python_file_names = ['models', 'views', 'urls', 'forms', 'admin']
    for name in python_file_names:
        create_python_file(app_name, name, fields)

    templates_file_names = ['base', 'list', 'new', 'show', 'edit']
    for name in templates_file_names:
        create_template_file(app_name, name, fields)


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = u'Custom command for generate apps'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('app_name', nargs='?', type=str)
        parser.add_argument('fields', nargs='*', type=str)

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        fields = options.get('fields', None)

        check_args_errors(app_name, fields)
        check_existing_app(app_name)
        fields = process_fields(fields)
        config_app(app_name, fields)

        self.stdout.write(self.style.SUCCESS(get_content_success(app_name)))
