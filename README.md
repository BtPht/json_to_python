# json_to_python

## What does it do ?

This scripts helps you deal with JSON files found in the wild without
schemas or documentation. With just an example you can generate python
code to parse and/or generate JSON files of the same type.

Here is an example of the results you can get with the scripts :
```json
{
  "first_name": "bertrand",
  "age": 99,
  "height": 2.71,
  "address": {
    "street": "Champs Élysées",
    "postal_code": "01234",
    "city": "London"
  },
  "friends": [
    "Alice",
    "Bob",
    "Carl"
  ]
}
```

The attrs dataclasses generated
```python
import attr
from pprint import pprint


@attr.s(auto_attribs=True)
class Address:  # 2
    city: str = attr.ib(default="London")
    postal_code: str = attr.ib(default="01234")
    street: str = attr.ib(default="Champs Élysées")


@attr.s(auto_attribs=True)
class RootClass:  # 1
    address: Address = attr.ib(default=Address())
    age: int = attr.ib(default=99)
    first_name: str = attr.ib(default="bertrand")
    friends: list[Friends] = attr.ib(default=[Friends()])
    height: float = attr.ib(default=2.71)


if __name__ == "__main__":
    pprint(attr.asdict(RootClass()))
```

Ot the Django Rest-framework serializers generated :
```python
from rest_framework import fields, serializers


class AddressSerializer(serializers.Serializer):  # 2
    city = fields.CharField()
    postal_code = fields.CharField()
    street = fields.CharField()


class RootSerializer:  # 1
    address = AddressSerializer()
    age = fields.IntegerField()
    first_name = fields.CharField()
    friends = FriendsSerializer(many=True)
    height = fields.FloatField()

```

### TODO:
- Add tests:
    * all the single types
    * single string of single type
    * flat dictionary

### ROADMAP:
- Add option to use :
    * json data as default values
    * empty defaults (str="", int=0)
    * no defaults at all
- Add option to merge similar classes :
    * not at all
    * based on type and name of attributes (more difficult that it seems)
- Handle command line options
    * -f input file
    * -o output file
    * --type=atts/serializers
    * --auto-format (using black)