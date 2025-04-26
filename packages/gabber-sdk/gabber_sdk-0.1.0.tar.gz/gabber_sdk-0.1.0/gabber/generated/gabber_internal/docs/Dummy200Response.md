# Dummy200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**phone_number** | [**PhoneNumber**](PhoneNumber.md) |  | [optional] 
**phone_connection** | [**PhoneConnection**](PhoneConnection.md) |  | [optional] 
**phone_number_type** | [**PhoneNumberType**](PhoneNumberType.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.dummy200_response import Dummy200Response

# TODO update the JSON string below
json = "{}"
# create an instance of Dummy200Response from a JSON string
dummy200_response_instance = Dummy200Response.from_json(json)
# print the JSON string representation of the object
print(Dummy200Response.to_json())

# convert the object into a dict
dummy200_response_dict = dummy200_response_instance.to_dict()
# create an instance of Dummy200Response from a dict
dummy200_response_from_dict = Dummy200Response.from_dict(dummy200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


