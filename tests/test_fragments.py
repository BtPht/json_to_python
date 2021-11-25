from pprint import pprint
from hypothesis import given, strategies as st
import string
from main import FullMapping


string_strategy = st.text(
    min_size=1,
    max_size=100,
    alphabet=st.characters(
        whitelist_categories=("L",), whitelist_characters=string.ascii_letters
    ),
)


def test_answer():
    assert True


@given(string_strategy, string_strategy)
def test_single_string(key, value):
    parsed = FullMapping.parse({key: value})

    assert len(parsed.classes) == 0
    assert len(parsed.root_class.attributes) == 1
    assert parsed.root_class.attributes[0].name == key.lower()
    assert parsed.root_class.attributes[0].attr_type == str


@given(string_strategy, st.integers())
def test_single_integer(key, value):
    parsed = FullMapping.parse({key: value})

    assert len(parsed.classes) == 0
    assert len(parsed.root_class.attributes) == 1
    assert parsed.root_class.attributes[0].name == key.lower()
    assert parsed.root_class.attributes[0].attr_type == int


@given(string_strategy, st.floats())
def test_single_float(key, value):
    parsed = FullMapping.parse({key: value})

    assert len(parsed.classes) == 0
    assert len(parsed.root_class.attributes) == 1
    assert parsed.root_class.attributes[0].name == key.lower()
    assert parsed.root_class.attributes[0].attr_type == float


@given(string_strategy, string_strategy)
def test_dict_single_key(list_name, dict_name):
    parsed = FullMapping.parse(
        {
            "test": "bertrand",
            "age": 28,
            "height": 1.83,
            dict_name: {
                "street": "Kungsgatan 9",
                "postal_code": "01450",
                "city": "Stockholm",
            },
            list_name: [
                "hello",
                "test",
                "Alice",
            ],
        }
    )

    assert len(parsed.classes) == 1
    assert len(parsed.root_class.attributes) == 5
    assert parsed.classes[0].name == dict_name.lower()
    assert len(parsed.classes[0].attributes) == 3
