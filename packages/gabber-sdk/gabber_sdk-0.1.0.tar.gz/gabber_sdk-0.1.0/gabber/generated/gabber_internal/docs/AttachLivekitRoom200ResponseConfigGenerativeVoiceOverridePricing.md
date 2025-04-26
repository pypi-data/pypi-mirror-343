# AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing

Pricing details for this voice

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price_per_second** | **str** | Price per second for using this voice | 
**currency** | **str** | Currency for the price (e.g., USD) | 
**product_name** | **str** | Name of the product in Stripe | 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_voice_override_pricing import AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing from a JSON string
attach_livekit_room200_response_config_generative_voice_override_pricing_instance = AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_voice_override_pricing_dict = attach_livekit_room200_response_config_generative_voice_override_pricing_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing from a dict
attach_livekit_room200_response_config_generative_voice_override_pricing_from_dict = AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing.from_dict(attach_livekit_room200_response_config_generative_voice_override_pricing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


