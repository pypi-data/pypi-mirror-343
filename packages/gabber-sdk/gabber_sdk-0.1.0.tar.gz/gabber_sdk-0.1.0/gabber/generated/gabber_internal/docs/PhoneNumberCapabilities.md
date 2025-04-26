# PhoneNumberCapabilities


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sms** | **bool** |  | 
**voice** | **bool** |  | 

## Example

```python
from gabber.generated.gabber_internal.models.phone_number_capabilities import PhoneNumberCapabilities

# TODO update the JSON string below
json = "{}"
# create an instance of PhoneNumberCapabilities from a JSON string
phone_number_capabilities_instance = PhoneNumberCapabilities.from_json(json)
# print the JSON string representation of the object
print(PhoneNumberCapabilities.to_json())

# convert the object into a dict
phone_number_capabilities_dict = phone_number_capabilities_instance.to_dict()
# create an instance of PhoneNumberCapabilities from a dict
phone_number_capabilities_from_dict = PhoneNumberCapabilities.from_dict(phone_number_capabilities_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


