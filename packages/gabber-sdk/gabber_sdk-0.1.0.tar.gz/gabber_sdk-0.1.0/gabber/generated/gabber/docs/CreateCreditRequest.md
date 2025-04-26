# CreateCreditRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the credit. | 
**description** | **str** | The description of the credit. | 
**allow_negative_balance** | **bool** | Whether the credit can have a negative balance. | 

## Example

```python
from gabber.generated.gabber.models.create_credit_request import CreateCreditRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCreditRequest from a JSON string
create_credit_request_instance = CreateCreditRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCreditRequest.to_json())

# convert the object into a dict
create_credit_request_dict = create_credit_request_instance.to_dict()
# create an instance of CreateCreditRequest from a dict
create_credit_request_from_dict = CreateCreditRequest.from_dict(create_credit_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


