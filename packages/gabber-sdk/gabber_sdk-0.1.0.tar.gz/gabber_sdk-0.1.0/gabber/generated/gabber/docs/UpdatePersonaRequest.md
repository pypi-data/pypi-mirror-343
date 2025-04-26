# UpdatePersonaRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**image_url** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**gender** | **str** |  | [optional] 
**voice** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.update_persona_request import UpdatePersonaRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdatePersonaRequest from a JSON string
update_persona_request_instance = UpdatePersonaRequest.from_json(json)
# print the JSON string representation of the object
print(UpdatePersonaRequest.to_json())

# convert the object into a dict
update_persona_request_dict = update_persona_request_instance.to_dict()
# create an instance of UpdatePersonaRequest from a dict
update_persona_request_from_dict = UpdatePersonaRequest.from_dict(update_persona_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


