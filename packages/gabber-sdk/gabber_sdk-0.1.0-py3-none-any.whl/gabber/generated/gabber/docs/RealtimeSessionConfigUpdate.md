# RealtimeSessionConfigUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | [**RealtimeSessionGeneralConfig**](RealtimeSessionGeneralConfig.md) |  | [optional] 
**input** | [**RealtimeSessionInputConfig**](RealtimeSessionInputConfig.md) |  | [optional] 
**generative** | [**RealtimeSessionGenerativeConfigUpdate**](RealtimeSessionGenerativeConfigUpdate.md) |  | [optional] 
**output** | [**RealtimeSessionOutputConfig**](RealtimeSessionOutputConfig.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.realtime_session_config_update import RealtimeSessionConfigUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionConfigUpdate from a JSON string
realtime_session_config_update_instance = RealtimeSessionConfigUpdate.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionConfigUpdate.to_json())

# convert the object into a dict
realtime_session_config_update_dict = realtime_session_config_update_instance.to_dict()
# create an instance of RealtimeSessionConfigUpdate from a dict
realtime_session_config_update_from_dict = RealtimeSessionConfigUpdate.from_dict(realtime_session_config_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


