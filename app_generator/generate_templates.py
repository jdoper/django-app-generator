# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


STYLES = "{% block styles %}"
CONTENT = "{% block content %}"
SCRIPTS = "{% block scripts %}"
ENDBLOCK = "{% endblock %}"

LOAD_STATIC = "{% load staticfiles %}"
TOKEN = "{% csrf_token %}"
FORM = "{{ form.as_p }}"

EMPTY = "{% empty %}"
ENDFOR = "{% endfor %}"


###################################
#             Auxiliares          #
###################################

def get_type_field(type_field):
    """
    Retorna o tipo de campo que vai ser inserido no models.py

    :param type_field: Tipo informado pelo usuário ao executar o comando scaffold
    :type type_field: str
    """

    types = {
        "character": "models.CharField(max_length=250)",
        "text": "models.TextField()",
        "integer": "models.IntegerField()",
        "float": "models.FloatField()",
        "decimal": "models.DecimalField(max_digits=5, decimal_places=2)"
        "boolean": "models.BooleanField()",
        "date": "models.DateField()",
        "datetime": "models.DateTimeField()",
        "slug": "models.SlugField()",
        "url": "models.URLField()",
    }
    return types.get(type_field, None)


def get_params(params):
    """
    Retorna os parâmetros essenciais para geração de um template

    :param params: Parâmetros personalizados de acordo com o tipo de página
    :type params: dict
    """

    default_params = {'styles': STYLES,
                    'content': CONTENT,
                    'scripts': SCRIPTS,
                    'endblock': ENDBLOCK,
                    'load_static': LOAD_STATIC}
    return dict(params.items() + default_params.items())


def get_load_base(app_name):
    """
    Retorna a tag para extender template base.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return mark_safe(u'{% extends "' + app_name + '/base.html" %}')


def get_id(app_name):
    """
    Retorna a tag para mostrar id do objeto

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return "{{ %s.id }}" % app_name


def get_for_tag(app_name):
    """
    Retorna a tag for customizada para listar registros no template list.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return "{% for " + app_name + " in " + app_name + "s %}"


def get_field_models(name_field, type_field):
    """
    Retorna um atributo da classe do models.py

    :param name_field: Nome do atributo
    :type name_field: str

    :param type_field: Tipo do atributo
    :type type_field: str
    """

    return "    %s = %s\n" % (name_field, get_type_field(type_field))


def get_field_tagtemplate(app_name, name_field):
    """
    Retorna uma tag para mostrar o valor do atributo de um objeto no template

    :param app_name: Nome do app que está sendo criado
    :type app_name: str

    :param name_field: Nome do atributo
    :type name_field: str
    """

    return "{{ %s.%s }}" % (app_name, name_field)


###################################
#          Arquivos Python        #
###################################

def get_content_views(app_name):
    """
    Retorna o conteudo para geração de um arquivo views.py

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return render_to_string('app_generator/python/views.txt', {'app': app_name})


def get_content_urls(app_name):
    """
    Retorna o conteudo para geração de um arquivo urls.py

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return render_to_string('app_generator/python/urls.txt', {'app': app_name})


def get_content_models(app_name, fields):
    """
    Retorna o conteudo para geração de um arquivo urls.py

    :param app_name: Nome do app que está sendo criado
    :type app_name: str

    :param fields: Lista dos campos passados ao executar o comando scaffold
    :type fields: list
    """

    fields_template = ""

    for field in fields:
        fields_template += get_field_models(field[0], field[1])

    return render_to_string('app_generator/python/models.txt', {'app': app_name,
                                                            'fields': fields_template})


def get_content_forms(app_name, fields):
    """
    Retorna o conteudo para geração de um arquivo forms.py

    :param app_name: Nome do app que está sendo criado
    :type app_name: str

    :param fields: Lista dos campos passados ao executar o comando scaffold
    :type fields: list
    """

    return render_to_string('app_generator/python/forms.txt', {'app': app_name,
                                                            'fields': fields})


def get_content_admin(app_name):
    """
    Retorna o conteudo para geração de um arquivo admin.py

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    return render_to_string('app_generator/python/admin.txt', {'app': app_name})


###################################
#           Arquivos HTML         #
###################################

def get_content_base():
    """
    Retorna o conteudo para geração de um arquivo base.html
    """

    base_params = {}
    params = get_params(base_params)

    return render_to_string('app_generator/html/base.txt', params)


def get_content_new(app_name):
    """
    Retorna o conteudo para geração de um arquivo novo.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    new_parms = {'load_base': get_load_base(app_name),
                'app': app_name,
                'token': TOKEN,
                'form': FORM}
    params = get_params(new_parms)

    return render_to_string('app_generator/html/new.txt', params)


def get_content_edit(app_name):
    """
    Retorna o conteudo para geração de um arquivo editar.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str
    """

    edit_params = {'load_base': get_load_base(app_name),
                    'app': app_name,
                    'token': TOKEN,
                    'form': FORM}
    params = get_params(edit_params)

    return render_to_string('app_generator/html/edit.txt', params)


def get_content_show(app_name, fields):
    """
    Retorna o conteudo para geração de um arquivo mostrar.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str

    :param fields: Lista dos campos passados ao executar o comando scaffold
    :type fields: list
    """

    for field in fields:
        field[1] = get_field_tagtemplate(app_name, field[0])

    show_params = {'load_base': get_load_base(app_name),
                    'app': app_name,
                    'id': get_id(app_name),
                    'fields': fields}
    params = get_params(show_params)

    return render_to_string('app_generator/html/show.txt', params)


def get_content_list(app_name, fields):
    """
    Retorna o conteudo para geração de um arquivo listar.html

    :param app_name: Nome do app que está sendo criado
    :type app_name: str

    :param fields: Lista dos campos passados ao executar o comando scaffold
    :type fields: list
    """

    for field in fields:
        field[1] = get_field_tagtemplate(app_name, field[0])

    list_params = {'load_base': get_load_base(app_name),
                    'app': app_name,
                    'id': get_id(app_name),
                    'fields': fields,
                    'for_tag': get_for_tag(app_name),
                    'empty_tag': EMPTY,
                    'endfor_tag': ENDFOR}
    params = get_params(list_params)

    return render_to_string('app_generator/html/list.txt', params)
