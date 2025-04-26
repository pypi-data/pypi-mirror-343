from dataclasses import dataclass


from gabber.generated import gabber as gabber_api

api_types = gabber_api


@dataclass
class Api:
    tool: gabber_api.ToolApi
    llm: gabber_api.LLMApi
    persona: gabber_api.PersonaApi
    scenario: gabber_api.ScenarioApi
    voice: gabber_api.VoiceApi
    realtime: gabber_api.RealtimeApi
    usage: gabber_api.UsageApi
    credit: gabber_api.CreditApi


def create_api(*, usage_token: str | None = None, api_key: str | None = None):
    if usage_token is None and api_key is None:
        raise ValueError("Either usage_token or api_key must be provided")

    if usage_token is not None and api_key is not None:
        raise ValueError("Only one of usage_token or api_key must be provided")

    api_configuration = gabber_api.Configuration(host="https://api.gabber.dev")
    api_client = gabber_api.ApiClient(configuration=api_configuration)
    if usage_token is not None:
        api_client.set_default_header("Authorization", f"Bearer {usage_token}")
    elif api_key is not None:
        api_client.set_default_header("x-api-key", api_key)

    tool = gabber_api.ToolApi(api_client)
    llm = gabber_api.LLMApi(api_client)
    persona = gabber_api.PersonaApi(api_client)
    scenario = gabber_api.ScenarioApi(api_client)
    voice = gabber_api.VoiceApi(api_client)
    realtime = gabber_api.RealtimeApi(api_client)
    credit = gabber_api.CreditApi(api_client)
    usage = gabber_api.UsageApi(api_client)

    return Api(
        tool=tool,
        llm=llm,
        persona=persona,
        scenario=scenario,
        voice=voice,
        realtime=realtime,
        usage=usage,
        credit=credit,
    )


__all__ = [
    "create_api",
    "Api",
    "api_types",
]
