# SDKConnectOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_details** | [**RealtimeSessionConnectionDetails**](RealtimeSessionConnectionDetails.md) |  | 
**token** | **str** |  | 
**config** | [**RealtimeSessionConfigCreate**](RealtimeSessionConfigCreate.md) |  | 

## Example

```python
from gabber.generated.gabber.models.sdk_connect_options import SDKConnectOptions

# TODO update the JSON string below
json = "{}"
# create an instance of SDKConnectOptions from a JSON string
sdk_connect_options_instance = SDKConnectOptions.from_json(json)
# print the JSON string representation of the object
print(SDKConnectOptions.to_json())

# convert the object into a dict
sdk_connect_options_dict = sdk_connect_options_instance.to_dict()
# create an instance of SDKConnectOptions from a dict
sdk_connect_options_from_dict = SDKConnectOptions.from_dict(sdk_connect_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


