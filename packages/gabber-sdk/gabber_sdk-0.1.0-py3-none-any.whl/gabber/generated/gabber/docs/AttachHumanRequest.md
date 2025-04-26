# AttachHumanRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**human** | **str** | The unique identifier of the Human. | 

## Example

```python
from gabber.generated.gabber.models.attach_human_request import AttachHumanRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AttachHumanRequest from a JSON string
attach_human_request_instance = AttachHumanRequest.from_json(json)
# print the JSON string representation of the object
print(AttachHumanRequest.to_json())

# convert the object into a dict
attach_human_request_dict = attach_human_request_instance.to_dict()
# create an instance of AttachHumanRequest from a dict
attach_human_request_from_dict = AttachHumanRequest.from_dict(attach_human_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


