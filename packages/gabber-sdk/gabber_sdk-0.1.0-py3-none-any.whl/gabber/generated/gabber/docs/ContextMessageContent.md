# ContextMessageContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**text** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.context_message_content import ContextMessageContent

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMessageContent from a JSON string
context_message_content_instance = ContextMessageContent.from_json(json)
# print the JSON string representation of the object
print(ContextMessageContent.to_json())

# convert the object into a dict
context_message_content_dict = context_message_content_instance.to_dict()
# create an instance of ContextMessageContent from a dict
context_message_content_from_dict = ContextMessageContent.from_dict(context_message_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


