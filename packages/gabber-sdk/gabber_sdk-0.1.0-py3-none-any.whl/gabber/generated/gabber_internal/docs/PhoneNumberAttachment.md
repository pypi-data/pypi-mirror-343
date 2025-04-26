# PhoneNumberAttachment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**number** | **str** |  | 
**project** | **str** |  | 
**phone_connection** | **str** |  | 
**persona** | **str** |  | [optional] 
**scenario** | **str** |  | [optional] 
**time_limit_s** | **int** |  | [optional] 
**llm** | **str** |  | 
**interruptable** | **bool** |  | 
**system_prompt** | **str** |  | [optional] 
**answer_message** | **str** |  | [optional] 
**voice_override** | **str** |  | [optional] 
**tool_definitions** | **List[str]** |  | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.phone_number_attachment import PhoneNumberAttachment

# TODO update the JSON string below
json = "{}"
# create an instance of PhoneNumberAttachment from a JSON string
phone_number_attachment_instance = PhoneNumberAttachment.from_json(json)
# print the JSON string representation of the object
print(PhoneNumberAttachment.to_json())

# convert the object into a dict
phone_number_attachment_dict = phone_number_attachment_instance.to_dict()
# create an instance of PhoneNumberAttachment from a dict
phone_number_attachment_from_dict = PhoneNumberAttachment.from_dict(phone_number_attachment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


