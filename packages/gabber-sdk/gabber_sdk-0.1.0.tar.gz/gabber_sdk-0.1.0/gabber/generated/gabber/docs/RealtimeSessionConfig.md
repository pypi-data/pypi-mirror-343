# RealtimeSessionConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | [**RealtimeSessionGeneralConfig**](RealtimeSessionGeneralConfig.md) |  | 
**input** | [**RealtimeSessionInputConfig**](RealtimeSessionInputConfig.md) |  | 
**generative** | [**RealtimeSessionGenerativeConfig**](RealtimeSessionGenerativeConfig.md) |  | 
**output** | [**RealtimeSessionOutputConfig**](RealtimeSessionOutputConfig.md) |  | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_config import RealtimeSessionConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionConfig from a JSON string
realtime_session_config_instance = RealtimeSessionConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionConfig.to_json())

# convert the object into a dict
realtime_session_config_dict = realtime_session_config_instance.to_dict()
# create an instance of RealtimeSessionConfig from a dict
realtime_session_config_from_dict = RealtimeSessionConfig.from_dict(realtime_session_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


