# RealtimeSessionOutputConfig

Configuration for the output of the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stream_transcript** | **bool** | Whether to stream agent spoken transcript or send full transcript when it&#39;s available all at once. | 
**speech_synthesis_enabled** | **bool** | Whether to enable speech synthesis for the RealtimeSession. | [default to True]
**answer_message** | **str** | The message for the agent to speak first when the human joins. If exluded the agent will not speak first. | [optional] 

## Example

```python
from gabber.generated.gabber.models.realtime_session_output_config import RealtimeSessionOutputConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionOutputConfig from a JSON string
realtime_session_output_config_instance = RealtimeSessionOutputConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionOutputConfig.to_json())

# convert the object into a dict
realtime_session_output_config_dict = realtime_session_output_config_instance.to_dict()
# create an instance of RealtimeSessionOutputConfig from a dict
realtime_session_output_config_from_dict = RealtimeSessionOutputConfig.from_dict(realtime_session_output_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


