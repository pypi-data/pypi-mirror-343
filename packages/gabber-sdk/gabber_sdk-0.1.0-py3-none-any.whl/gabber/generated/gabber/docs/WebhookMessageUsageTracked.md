# WebhookMessageUsageTracked


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**payload** | [**WebhookMessageUsageTrackedPayload**](WebhookMessageUsageTrackedPayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_usage_tracked import WebhookMessageUsageTracked

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageUsageTracked from a JSON string
webhook_message_usage_tracked_instance = WebhookMessageUsageTracked.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageUsageTracked.to_json())

# convert the object into a dict
webhook_message_usage_tracked_dict = webhook_message_usage_tracked_instance.to_dict()
# create an instance of WebhookMessageUsageTracked from a dict
webhook_message_usage_tracked_from_dict = WebhookMessageUsageTracked.from_dict(webhook_message_usage_tracked_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


