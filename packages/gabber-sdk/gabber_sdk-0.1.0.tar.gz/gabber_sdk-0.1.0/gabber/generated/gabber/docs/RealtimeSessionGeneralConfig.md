# RealtimeSessionGeneralConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_limit_s** | **int** | The time limit in seconds for the RealtimeSession. | [optional] 
**save_messages** | **bool** | Whether to save messages in the RealtimeSession. These will be saved to the context provided in the generative config. If no context is provided, a new context will be created when the session starts.  | [default to True]

## Example

```python
from gabber.generated.gabber.models.realtime_session_general_config import RealtimeSessionGeneralConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionGeneralConfig from a JSON string
realtime_session_general_config_instance = RealtimeSessionGeneralConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionGeneralConfig.to_json())

# convert the object into a dict
realtime_session_general_config_dict = realtime_session_general_config_instance.to_dict()
# create an instance of RealtimeSessionGeneralConfig from a dict
realtime_session_general_config_from_dict = RealtimeSessionGeneralConfig.from_dict(realtime_session_general_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


