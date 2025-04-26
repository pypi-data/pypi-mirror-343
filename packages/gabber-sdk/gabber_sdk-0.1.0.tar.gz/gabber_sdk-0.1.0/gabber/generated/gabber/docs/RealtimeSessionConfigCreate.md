# RealtimeSessionConfigCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | [**RealtimeSessionGeneralConfig**](RealtimeSessionGeneralConfig.md) |  | 
**input** | [**RealtimeSessionInputConfig**](RealtimeSessionInputConfig.md) |  | 
**generative** | [**RealtimeSessionGenerativeConfigCreate**](RealtimeSessionGenerativeConfigCreate.md) |  | 
**output** | [**RealtimeSessionOutputConfig**](RealtimeSessionOutputConfig.md) |  | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_config_create import RealtimeSessionConfigCreate

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionConfigCreate from a JSON string
realtime_session_config_create_instance = RealtimeSessionConfigCreate.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionConfigCreate.to_json())

# convert the object into a dict
realtime_session_config_create_dict = realtime_session_config_create_instance.to_dict()
# create an instance of RealtimeSessionConfigCreate from a dict
realtime_session_config_create_from_dict = RealtimeSessionConfigCreate.from_dict(realtime_session_config_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


