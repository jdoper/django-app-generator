# -*- coding: utf-8 -*-
import os


def create_app(app_name):
    command = "python manage.py startapp %s" % app_name
    os.system(command)


def create_folder(app_name, name_folder):
    os.makedirs("%s/%s" % (app_name, name_folder))


def create_file(file_path, name_file, template):
    if os.path.exists(file_path):
        temp_file = "%s%s" % (file_path, name_file)

        with open(temp_file, 'w+') as python_file:
            python_file.write(template.encode('utf-8'))
            python_file.close()
