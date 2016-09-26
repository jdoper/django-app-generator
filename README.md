#django-app-generator

Package for generate apps in Django projects


### Installation

```sh
$ pip install git+https://github.com/jdoper/django-app-generator.git@master
```


### Usage

```sh
$ python manage.py scaffold app_name name_field:type_field
```
***OBS:*** Your allowed to use more than a model field in your command.


### Model Fields Available

* character - CharField
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

***0.2***
* Adding support to SlugField and URLField.

***0.1***
* Initial release.


### License

The MIT License.
