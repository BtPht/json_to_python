import abc

from json_parser import FullMapping, SimpleAttribute, SimpleClass

try:
    from black import Mode, format_str
except ImportError:

    def format_str(src_contents: str, _):
        return src_contents

    class Mode:
        pass


def camel_case(name: str) -> str:
    return "".join(list(map(lambda x: x.capitalize(), name.split("_"))))


class BaseFormater(abc.ABC):
    use_default: bool
    use_black: bool
    import_block = ""
    main_block = ""

    def __init__(self, default=True, black=True):
        self.use_default = default
        self.use_black = black
        super(BaseFormater, self).__init__()

    def to_str(self, mapping: FullMapping) -> str:
        ret = self.import_block
        for c in sorted(mapping.classes, key=lambda x: x.depth, reverse=True):
            ret += self._class_to_str(c)
        ret += self._class_to_str(mapping.root_class)
        ret += self.main_block

        if self.use_black:
            return format_str(ret, mode=Mode())
        return ret

    def _class_to_str(self, inner_class: SimpleClass) -> str:
        pass


class AttrsFormater(BaseFormater):

    import_block = "import attr\nfrom pprint import pprint\n"
    main_block = f"if __name__ == '__main__':\n{4*' '}pprint(attr.asdict(RootClass()))"

    def _class_to_str(self, inner_class: SimpleClass) -> str:
        ret = "@attr.s(auto_attribs=True)\n"
        if inner_class.name:
            ret += f"class {camel_case(inner_class.name)}: #{inner_class.depth}\n"
        else:
            ret += f"class RootClass: #{inner_class.depth}\n"
        for _a in sorted(inner_class.attributes, key=lambda x: x.name):
            ret += 4 * " " + self._attribute_to_str(_a)
        return ret

    def _attribute_to_str(self, attribute: SimpleAttribute) -> str:
        if attribute.attr_type.__qualname__ == "ListType":
            _type = f"list[{getattr(attribute.attr_type, 'sub_type')}]"
        else:
            _type = attribute.attr_type.__name__

        if self.use_default:
            if attribute.attr_type is str:
                value = f'"{attribute.value}"'  # generates a string with quotes
            elif attribute.attr_type in [int, float]:
                value = str(attribute.value)
            elif attribute.attr_type.__qualname__ == "ListType":
                value = f"[{getattr(attribute.attr_type, 'sub_type')}()]"
            else:
                value = f"{attribute.attr_type.__name__}()"
            default = "default=" + value
        else:
            default = ""

        if attribute.name.islower():
            noqa = ""
        else:
            noqa = "#noqa"  # for capitals in attribute names

        return f"{attribute.name}:{_type}=attr.ib({default}){noqa}\n"


class SerializerFormater(BaseFormater):

    import_block = "from rest_framework import fields, serializers\n"
    main_block = ""

    def get_serializer_by_type(self, attribute_type: type) -> str:
        if attribute_type is str:
            return "fields.CharField"
        elif attribute_type is float:
            return "fields.FloatField"
        elif attribute_type is int:
            return "fields.IntegerField"
        elif attribute_type is bool:
            return "fields.BooleanField"
        else:
            if hasattr(attribute_type, "__name__"):
                return attribute_type.__name__ + "Serializer"
            else:
                return str(attribute_type) + "Serializer"

    def _class_to_str(self, inner_class: SimpleClass) -> str:
        if inner_class.name:
            ret = f"class {camel_case(inner_class.name)}Serializer(serializers.Serializer): #{inner_class.depth}\n"
        else:
            ret = f"class RootSerializer: #{inner_class.depth}\n"
        for _a in sorted(inner_class.attributes, key=lambda x: x.name):
            ret += 4 * " " + self._attribute_to_str(_a)
        return ret

    def _attribute_to_str(self, attribute: SimpleAttribute) -> str:
        if attribute.attr_type.__qualname__ == "ListType":
            field = self.get_serializer_by_type(
                getattr(attribute.attr_type, "sub_type")
            )
            many = "many=True"
        else:
            field = self.get_serializer_by_type(attribute.attr_type)
            many = ""
        return f"{attribute.name}={field}({many})\n"
