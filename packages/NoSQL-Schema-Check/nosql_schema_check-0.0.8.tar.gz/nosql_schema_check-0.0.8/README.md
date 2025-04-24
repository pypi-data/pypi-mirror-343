# NoSQL-Schema-Check

## pip install NoSQL_Schema_Check

from nosql_schema_check.model import Model

class Model_Class(Model):

&nbsp;&nbsp;&nbsp;&nbsp;Schema={field: value}

&nbsp;&nbsp;&nbsp;&nbsp;Validations={field: function -> True/False}

&nbsp;&nbsp;&nbsp;&nbsp;Default={field: function -> Default value}

&nbsp;&nbsp;&nbsp;&nbsp;Required=[keys, ...]

&nbsp;&nbsp;Optional variable -

&nbsp;&nbsp;&nbsp;&nbsp;collection=Collection object.

Model_Class.generate()

---

Schema = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": 'type', -> change 'type' with type string.
    
&nbsp;&nbsp;&nbsp;&nbsp;"key1": {key: value, ...},
    
&nbsp;&nbsp;&nbsp;&nbsp;"key2": ('list', 'type') -> change 'type' with type string. ([value1, value2, ...])

}

---

Validations = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": validate function for value,
    
&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;validation for 'type' only.

}

---

Default = {
    
&nbsp;&nbsp;&nbsp;&nbsp;"key": function that returns default value,

&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;default value for field only.

}

---

functions - 

&nbsp;&nbsp;&nbsp;Model_Class.check_data

&nbsp;&nbsp;&nbsp;Model_Class.print_schema

&nbsp;&nbsp;&nbsp;Model_Class.compare_records

&nbsp;&nbsp;&nbsp;Model_Class.compare_record

&nbsp;&nbsp;&nbsp;Model_Class.update_records

&nbsp;&nbsp;&nbsp;Model_Class.update_record

&nbsp;&nbsp;&nbsp;Model_Class.collection

---

Example:
```python
class Test(Model):
    Schema={
        "integer": "int",
        "string": "str",
        "list": ('list', "int"),
        "dict": {
            "key": "int", 
            "key1": ('list', {
                "integer": "int", 
                "list": ('list', 'str')
            })
        },
        "list_in_list": ('list', ('list', "str")),
        "dict_in_dict": {
            "a": 'int',
            "b": {
                "a": 'str'
            }
        }
    }
    Validations={
        "integer": lambda i:True if i < 10 else print("Integer must be less than 10."),
        "string": lambda s: len(s) < 10,
        "list": (lambda l: len(l) < 4, lambda i: i < 10),
        "dict":(lambda d: len(d) < 3,
            {
                "key": lambda i: i < 10,
                "key1": (lambda l: len(l) < 2,)
            }),
        "list_in_list": lambda s: len(s) < 10,
        "dict_in_dict": {
            "b": {
                "a": lambda s: len(s) < 20,
            },
            "a":lambda i: i < 20
        }
    }
    Required=["integer", "list", ('dict', ["key", ("key1", ["integer"])])]
    Default={"string":lambda:"Default_String"[:9]}
    name="test"

Test.generate()

try:
    data = Test.compare_record({"integer": 9, "list": [2,3,5], "dict": {"key": 9, "key1": [{"integer": 20, "list": ["asdd", "sfd"]}]}, "list_in_list": [["string1", "string2", "string3"]], "Something": "Extra_Thing"}, True)
    print(data)
    data.pop("Something")
    print(Test.compare_records([data]))
    print(Test.update_record({"integer": 5, "list": [10,20,30]}, data))
    print(Test.update_records([{"integer": 5, "list": [10,20,30]},], [data,]))
except:
    pass
```