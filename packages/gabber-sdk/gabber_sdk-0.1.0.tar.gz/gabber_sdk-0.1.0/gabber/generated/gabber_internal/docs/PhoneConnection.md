# PhoneConnection


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**project** | **str** |  | 
**twilio_account_sid** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.phone_connection import PhoneConnection

# TODO update the JSON string below
json = "{}"
# create an instance of PhoneConnection from a JSON string
phone_connection_instance = PhoneConnection.from_json(json)
# print the JSON string representation of the object
print(PhoneConnection.to_json())

# convert the object into a dict
phone_connection_dict = phone_connection_instance.to_dict()
# create an instance of PhoneConnection from a dict
phone_connection_from_dict = PhoneConnection.from_dict(phone_connection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


