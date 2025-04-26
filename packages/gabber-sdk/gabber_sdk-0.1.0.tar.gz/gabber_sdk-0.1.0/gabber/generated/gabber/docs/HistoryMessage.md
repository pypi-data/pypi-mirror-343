# HistoryMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | 
**import_id** | **str** |  | [optional] 
**role** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.history_message import HistoryMessage

# TODO update the JSON string below
json = "{}"
# create an instance of HistoryMessage from a JSON string
history_message_instance = HistoryMessage.from_json(json)
# print the JSON string representation of the object
print(HistoryMessage.to_json())

# convert the object into a dict
history_message_dict = history_message_instance.to_dict()
# create an instance of HistoryMessage from a dict
history_message_from_dict = HistoryMessage.from_dict(history_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


