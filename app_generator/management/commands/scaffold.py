# -*- coding: utf-8 -*-
import os, shutil, re

from django.core.management.base import BaseCommand, CommandError

from app_generator.generate_content import *
from app_generator.generate_files import *


# Auxiliares #
def process_arg(arg):
    return "".join(re.split("[^a-zA-Z]*", arg))


# Geradores de arquivos #
def create_python_file(app_name, name_file, fields):
    template = get_content_python(app_name, name_file, fields)
    file_path = "%s/" % (app_name)
    name_file = "%s.py" % (name_file)
    create_file(file_path, name_file, template)


def create_template_file(app_name, name_file, fields):
    template = get_content_template(app_name, name_file, fields)
    file_path = "%s/templates/%s/" % (app_name, app_name)
    name_file = "%s.html" % (name_file)
    create_file(file_path, name_file, template)


# Geradores de conteudos #
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


# Verificadores #
def check_args(args):
    if len(args) >= 2:
        app_name = args.pop(0)
        fields, check = [], []

        for arg in args:
            variavel = arg.split(':')
            name = process_arg(variavel[0])
            field_type = variavel[1]

            if len(variavel) != 2:
                print "ERROR: A variavel -%s- não está no formato nome:tipo\n" % (name)
                return False
            elif len(name) < 2:
                print "ERROR: O nome da variavel -%s- deve ter pelo menos 2 caracteres\n" % (name)
                return False
            elif not get_model_field(field_type):
                print "ERROR: Verifique o tipo da variavel -%s- (tipo -%s- não existe)\n" % (name, field_type)
                return False
            elif name in check:
                print "ERROR: A variavel -%s- foi citada mais de uma vez\n" % (name)
                return False
            else:
                fields.append([name, field_type])
                check.append(name)

        return config_app(app_name, fields)
    else:
        print "ERRO: Verifique a quantidade de parametros passados"
        return False


def check_fields_errors(fields):
    pattern = re.compile("^[a-z_]+:[a-z]+")

    for field in fields:
        if not bool(pattern.match(field)):
            return field

    return None


def config_app(app_name, fields):
    path = "%s/" % app_name

    if os.path.exists(path):
        decision = raw_input("Existe outro app com o mesmo nome, deseja exclui-lo? (S/n) ")

        while decision != 'S' and decision != 'n':
            print "ERROR: O valor inserido é inválido"
            decision = raw_input("Existe outro app com o mesmo nome, deseja exclui-lo? (S/n) ")

        if decision == 'n':
            return False
        else:
            shutil.rmtree(path)

    create_app(app_name)
    create_folder(app_name, "templates")
    create_folder(app_name, "templates/%s" % (app_name))

    python_file_names = ['models', 'views', 'urls', 'forms', 'admin']
    for name in python_file_names:
        create_python_file(app_name, name, fields)

    templates_file_names = ['base', 'list', 'new', 'show', 'edit']
    for name in templates_file_names:
        create_template_file(app_name, name, fields)

    return True


class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = u'Custom command for generate apps'

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='*', type=str)
        parser.add_argument('fields', nargs='*', type=str)

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        fields = options.get('fields', None)

        if not app_name:
            raise CommandError('defina um nome para seu app')
        elif not app_name[0].isalpha():
            raise CommandError('app_name deve conter apenas letras (Ex: %s)' % process_arg(app_name))
        elif not fields:
            raise CommandError(u'não foram definidos campos para seu app')
        else:
            check = check_fields_errors(fields)

            if check:
                raise CommandError(u'"%s" não está no formato name_field:type_field' % check)
            else:
                print "OK pode começar a putaria"

        if check_args(list(args)):
            print "App criado com sucesso!\n"

            print "INFO: Adicione a linha abaixo no seu arquivo settings.py"
            print "'%s',\n" % (process_arg(args[0]))

            print "INFO: Adicione a linha abaixo no seu arquivo urls.py"
            print "url(r'^%s/', include('%s.urls'), name=''),\n" % (process_arg(args[0]), process_arg(args[0]))
