# SDKSendChatMessageParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.sdk_send_chat_message_params import SDKSendChatMessageParams

# TODO update the JSON string below
json = "{}"
# create an instance of SDKSendChatMessageParams from a JSON string
sdk_send_chat_message_params_instance = SDKSendChatMessageParams.from_json(json)
# print the JSON string representation of the object
print(SDKSendChatMessageParams.to_json())

# convert the object into a dict
sdk_send_chat_message_params_dict = sdk_send_chat_message_params_instance.to_dict()
# create an instance of SDKSendChatMessageParams from a dict
sdk_send_chat_message_params_from_dict = SDKSendChatMessageParams.from_dict(sdk_send_chat_message_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


