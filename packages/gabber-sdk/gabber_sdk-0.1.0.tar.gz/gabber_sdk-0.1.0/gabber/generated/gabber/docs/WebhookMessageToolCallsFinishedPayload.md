# WebhookMessageToolCallsFinishedPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**realtime_session** | **str** |  | [optional] 
**group** | **str** |  | 
**tool_calls** | [**List[WebhookMessageToolCall]**](WebhookMessageToolCall.md) |  | 
**tool_call_results** | [**List[ToolCallResult]**](ToolCallResult.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_calls_finished_payload import WebhookMessageToolCallsFinishedPayload

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCallsFinishedPayload from a JSON string
webhook_message_tool_calls_finished_payload_instance = WebhookMessageToolCallsFinishedPayload.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCallsFinishedPayload.to_json())

# convert the object into a dict
webhook_message_tool_calls_finished_payload_dict = webhook_message_tool_calls_finished_payload_instance.to_dict()
# create an instance of WebhookMessageToolCallsFinishedPayload from a dict
webhook_message_tool_calls_finished_payload_from_dict = WebhookMessageToolCallsFinishedPayload.from_dict(webhook_message_tool_calls_finished_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


