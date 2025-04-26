# WebhookMessageUsageTrackedPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | [**UsageType**](UsageType.md) |  | 
**value** | **float** |  | 
**human** | **str** |  | [optional] 
**project** | **str** |  | 
**metadata** | **object** |  | [optional] 
**human_id** | **str** | Use &#x60;human&#x60; instead. | [optional] 
**extra** | **object** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.webhook_message_usage_tracked_payload import WebhookMessageUsageTrackedPayload

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageUsageTrackedPayload from a JSON string
webhook_message_usage_tracked_payload_instance = WebhookMessageUsageTrackedPayload.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageUsageTrackedPayload.to_json())

# convert the object into a dict
webhook_message_usage_tracked_payload_dict = webhook_message_usage_tracked_payload_instance.to_dict()
# create an instance of WebhookMessageUsageTrackedPayload from a dict
webhook_message_usage_tracked_payload_from_dict = WebhookMessageUsageTrackedPayload.from_dict(webhook_message_usage_tracked_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


