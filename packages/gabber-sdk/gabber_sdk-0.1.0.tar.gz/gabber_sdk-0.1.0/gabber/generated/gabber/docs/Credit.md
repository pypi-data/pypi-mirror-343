# Credit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | The date and time the credit was created. | 
**id** | **str** | The unique identifier of the credit. | 
**project** | **str** | The project the credit belongs to. | 
**name** | **str** | The name of the credit. | 
**description** | **str** | The description of the credit. | 
**allow_negative_balance** | **bool** | Whether the credit can have a negative balance. | 

## Example

```python
from gabber.generated.gabber.models.credit import Credit

# TODO update the JSON string below
json = "{}"
# create an instance of Credit from a JSON string
credit_instance = Credit.from_json(json)
# print the JSON string representation of the object
print(Credit.to_json())

# convert the object into a dict
credit_dict = credit_instance.to_dict()
# create an instance of Credit from a dict
credit_from_dict = Credit.from_dict(credit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


