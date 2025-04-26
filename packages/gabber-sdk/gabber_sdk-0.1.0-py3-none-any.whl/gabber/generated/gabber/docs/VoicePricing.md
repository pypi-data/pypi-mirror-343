# VoicePricing

Pricing details for a voice

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**price_per_second** | **str** | Price per second for using this voice | 
**currency** | **str** | Currency for the price (e.g., USD) | 
**product_name** | **str** | Name of the product in Stripe | 

## Example

```python
from gabber.generated.gabber.models.voice_pricing import VoicePricing

# TODO update the JSON string below
json = "{}"
# create an instance of VoicePricing from a JSON string
voice_pricing_instance = VoicePricing.from_json(json)
# print the JSON string representation of the object
print(VoicePricing.to_json())

# convert the object into a dict
voice_pricing_dict = voice_pricing_instance.to_dict()
# create an instance of VoicePricing from a dict
voice_pricing_from_dict = VoicePricing.from_dict(voice_pricing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


