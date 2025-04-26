# RealtimeSessionInputConfig

Configuration for the output of the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interruptable** | **bool** | Whether the system allows interruption during speech. | [default to True]
**parallel_listening** | **bool** | Whether the AI should continue listening while speaking. If true, the AI will produce another response immediately after the first one. This is only relevant if interruptable is false.  | [default to False]

## Example

```python
from gabber.generated.gabber.models.realtime_session_input_config import RealtimeSessionInputConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionInputConfig from a JSON string
realtime_session_input_config_instance = RealtimeSessionInputConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionInputConfig.to_json())

# convert the object into a dict
realtime_session_input_config_dict = realtime_session_input_config_instance.to_dict()
# create an instance of RealtimeSessionInputConfig from a dict
realtime_session_input_config_from_dict = RealtimeSessionInputConfig.from_dict(realtime_session_input_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


