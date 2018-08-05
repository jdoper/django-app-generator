# django-app-generator

Package for generate apps in Django projects


### Installation

```sh
$ pip install git+https://github.com/jdoper/django-app-generator.git@master
```

Add 'app_generator' to your INSTALLED_APPS setting.
```sh
INSTALLED_APPS = (
    ...
    'app_generator',
)
```


### Usage

```sh
$ python manage.py scaffold app_name name_field:type_field
```
Your allowed to use more than a model field in your command.


### Model Fields Available

* char - CharField
* text - TextField
* integer - IntegerField
* float - FloatField
* decimal - DecimalField
* boolean - BooleanField
* date - DateField
* datetime - DateTimeField
* slug - SlugField
* url - URLField


### Changelog

***0.1***
* Initial release.


### License

The MIT License.
