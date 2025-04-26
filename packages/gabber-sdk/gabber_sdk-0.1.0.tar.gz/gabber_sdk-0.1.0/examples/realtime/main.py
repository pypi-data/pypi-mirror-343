import logging
import asyncio
import gabber
import os
import wave

GABBER_API_KEY = os.environ["GABBER_API_KEY"]


async def mock_backend_handler():
    """
    Never(!!!) use your api key on the client side, instead use a backend service to generate the client token.
    Here we are mocking what your backend handler might do.
    """
    if GABBER_API_KEY is None:
        raise ValueError("GABBER_API_KEY environment variable not set")

    user_id = "some_user_id"
    api = gabber.create_api(api_key=GABBER_API_KEY)
    req = gabber.api_types.UsageTokenRequest(human=user_id)
    token_res = await api.usage.create_usage_token(req)
    context_res = await api.llm.create_context(
        context_create_request=gabber.api_types.ContextCreateRequest(
            messages=[
                gabber.api_types.ContextMessageCreateParams(
                    role="system",
                    content="You are a toy for kids! Be fun and playful.",
                ),
            ]
        ),
        x_human_id=user_id,
    )

    return {"token": token_res.token, "context": context_res.id}


class GabberHandler(gabber.realtime_session.RealtimeSessionHandler):
    def __init__(self, *, connected_future: asyncio.Future[None]):
        super().__init__()
        self._connected_future = connected_future
        self._messages = []

    def messages_changed(self, messages):
        self._messages = messages

    def agent_error(self, msg: str):
        logging.error(f"Agent error: {msg}")

    def remaining_seconds_changed(self, seconds: int):
        pass

    def agent_state_changed(self, state: gabber.api_types.SDKAgentState):
        logging.info(f"Agent state changed: {state}")

    def connection_state_changed(self, state: gabber.api_types.SDKConnectionState):
        logging.info(f"Connection state changed: {state}")
        if state == gabber.api_types.SDKConnectionState.CONNECTED:
            print("NEIL setting res")
            self._connected_future.set_result(None)


async def main():
    connected_future = asyncio.Future[None]()
    gabber_realtime_session = gabber.realtime_session.RealtimeSession(
        handler=GabberHandler(connected_future=connected_future)
    )

    backend_res = await mock_backend_handler()
    usage_token = backend_res["token"]
    context_id = backend_res["context"]
    config = gabber.api_types.RealtimeSessionConfigCreate(
        general=gabber.api_types.RealtimeSessionGeneralConfig(
            save_messages=True,
        ),
        input=gabber.api_types.RealtimeSessionInputConfig(
            interruptable=True,
            parallel_listening=True,
        ),
        generative=gabber.api_types.RealtimeSessionGenerativeConfigCreate(
            llm="9e467988-a82b-4c72-bb26-62522b78f2e0",  # Gabber 70B
            voice_override="626c3b02-2d2a-4a93-b3e7-be35fd2b95cd",  # Tara,
            context=context_id,
            tool_definitions=[],  # For tool calls
        ),
        output=gabber.api_types.RealtimeSessionOutputConfig(
            stream_transcript=False,  # Save some bandwidth
            speech_synthesis_enabled=True,
        ),
    )
    opts = gabber.api_types.SDKConnectOptions()
    ut_opts = gabber.api_types.SDKConnectOptionsOneOf1(token=usage_token, config=config)
    opts.actual_instance = ut_opts
    await gabber_realtime_session.connect(opts=opts)

    logging.info(
        "Connected to the Gabber Realtime Session, waiting for agent to join..."
    )

    await connected_future

    logging.info("Agent joined!")

    async def receive_task():
        with wave.open("agent_output.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            async for audio_bytes in gabber_realtime_session.audio_stream:
                wf.writeframes(audio_bytes)

        logging.info("Receive task finished")

    rt = asyncio.create_task(receive_task())
    try:
        while True:
            logging.info("Simulating user audio input from 'hello_world.wav'")
            with wave.open("hello_world.wav", "rb") as wf:
                audio_data = wf.readframes(wf.getnframes())
                gabber_realtime_session.microphone.push_audio(audio_data)
            await asyncio.sleep(20)

    except KeyboardInterrupt:
        logging.info("Stopping the session")
        await gabber_realtime_session.disconnect()

    await rt

    logging.info("Goodbye!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
