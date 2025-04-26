# SDKConnectOptionsOneOf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_details** | [**RealtimeSessionConnectionDetails**](RealtimeSessionConnectionDetails.md) |  | 

## Example

```python
from gabber.generated.gabber.models.sdk_connect_options_one_of import SDKConnectOptionsOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of SDKConnectOptionsOneOf from a JSON string
sdk_connect_options_one_of_instance = SDKConnectOptionsOneOf.from_json(json)
# print the JSON string representation of the object
print(SDKConnectOptionsOneOf.to_json())

# convert the object into a dict
sdk_connect_options_one_of_dict = sdk_connect_options_one_of_instance.to_dict()
# create an instance of SDKConnectOptionsOneOf from a dict
sdk_connect_options_one_of_from_dict = SDKConnectOptionsOneOf.from_dict(sdk_connect_options_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


