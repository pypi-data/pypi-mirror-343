# SDKConnectOptionsOneOf1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** |  | 
**config** | [**RealtimeSessionConfigCreate**](RealtimeSessionConfigCreate.md) |  | 

## Example

```python
from gabber.generated.gabber.models.sdk_connect_options_one_of1 import SDKConnectOptionsOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of SDKConnectOptionsOneOf1 from a JSON string
sdk_connect_options_one_of1_instance = SDKConnectOptionsOneOf1.from_json(json)
# print the JSON string representation of the object
print(SDKConnectOptionsOneOf1.to_json())

# convert the object into a dict
sdk_connect_options_one_of1_dict = sdk_connect_options_one_of1_instance.to_dict()
# create an instance of SDKConnectOptionsOneOf1 from a dict
sdk_connect_options_one_of1_from_dict = SDKConnectOptionsOneOf1.from_dict(sdk_connect_options_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


