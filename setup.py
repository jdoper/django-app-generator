import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-app-generator',
    version='0.1',
    description='Package for generate apps in Django projects',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=README,
    author='João Pedro Araújo',
    author_email='medeiros.jparaujo@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    url='https://github.com/jdoper/django-app-generator',
)
