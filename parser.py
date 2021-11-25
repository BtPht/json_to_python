import typing

import attr


def camel_case(name: str) -> str:
    return "".join(list(map(lambda x: x.capitalize(), name.split("_"))))


class ListType(type):
    sub_type: type

    def __new__(cls, sub_type):
        cls = super(ListType, cls).__new__(cls, "ListType", (list,), {})
        cls.sub_type = sub_type
        return cls

    @property
    def __name__(self):
        return str(self.sub_type)

    def __class__(self):
        return ListType


@attr.s(auto_attribs=True)
class SimpleAttribute:
    name: str = attr.ib(converter=lambda x: x.replace(" ", "_"))
    attr_type: type
    value: typing.Any = None


@attr.s(auto_attribs=True)
class SimpleClass:
    """
    A SimplClass is a class that contains only simple attributes
    """

    name: str = attr.ib(eq=False, converter=lambda x: x.lower().replace("-", "_"))
    attributes: attr.ib(
        type=list[SimpleAttribute], default=attr.Factory(SimpleAttribute)
    )
    depth: attr.ib(eq=int, type=int, default=0)

    def is_identical(self, other_class: "SimpleClass") -> bool:
        for other_attribute in other_class.attributes:
            if not self.has_attribute(other_attribute):
                return False
        return True

    def has_attribute(self, other_attribue: SimpleAttribute) -> bool:
        for my_attribute in self.attributes:
            if (
                my_attribute.attr_type == other_attribue.attr_type
                and my_attribute.name == other_attribue.name
            ):
                return True
        return False


@attr.s(auto_attribs=True)
class FullMapping:
    root_class: attr.ib(type=SimpleClass, default=attr.Factory(SimpleClass))
    classes: attr.ib(type=list[SimpleClass], default=attr.Factory(list))

    @classmethod
    def parse(cls, input_dict: dict, name: str = "", depth=0) -> "FullMapping":
        if all(list(map(lambda x: type(x) not in [dict, list], input_dict.values()))):
            # we know there is no nested object at this level
            __root_class = SimpleClass(
                name,
                list(
                    map(
                        lambda x: SimpleAttribute(x[0], type(x[1]), x[1]),
                        list(input_dict.items()),
                    ),
                ),
                depth + 1,
            )
            return cls(__root_class, [])
        _root_class = SimpleClass(name, [], depth + 1)
        _classes_list = []
        for k, v in input_dict.items():
            if type(v) is dict:
                mapping = FullMapping.parse(v, k, depth + 1)
                _classes_list.append(mapping.root_class)
                _classes_list.extend(mapping.classes)
                _root_class.attributes.append(
                    SimpleAttribute(
                        k.lower(),
                        type(camel_case(mapping.root_class.name), (object,), {}),
                        camel_case(mapping.root_class.name),
                    )
                )
            elif type(v) is list:
                if len(v) > 0:
                    if type(v[0]) in [dict, list]:
                        mapping = FullMapping.parse(
                            {k.capitalize(): v[0]}, name, depth + 1
                        )
                        _classes_list.extend(mapping.classes)
                    _root_class.attributes.append(
                        SimpleAttribute(k, ListType(k.capitalize()), [])
                    )
                else:
                    _root_class.attributes.append(SimpleAttribute(k, list, []))
            else:
                _root_class.attributes.append(SimpleAttribute(k.lower(), type(v), v))
        return cls(_root_class, _classes_list)
