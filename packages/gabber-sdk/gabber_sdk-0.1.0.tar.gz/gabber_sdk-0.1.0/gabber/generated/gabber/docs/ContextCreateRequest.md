# ContextCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**persona** | **str** |  | [optional] 
**scenario** | **str** |  | [optional] 
**messages** | [**List[ContextMessageCreateParams]**](ContextMessageCreateParams.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.context_create_request import ContextCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ContextCreateRequest from a JSON string
context_create_request_instance = ContextCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ContextCreateRequest.to_json())

# convert the object into a dict
context_create_request_dict = context_create_request_instance.to_dict()
# create an instance of ContextCreateRequest from a dict
context_create_request_from_dict = ContextCreateRequest.from_dict(context_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


