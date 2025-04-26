import asyncio
from typing import cast
import logging
from gabber.api import create_api, api_types
from livekit import rtc
from abc import ABC, abstractmethod
import json


class RealtimeSessionHandler(ABC):
    @abstractmethod
    def connection_state_changed(self, state: api_types.SDKConnectionState):
        pass

    @abstractmethod
    def agent_state_changed(self, state: api_types.SDKAgentState):
        pass

    @abstractmethod
    def remaining_seconds_changed(self, seconds: int):
        pass

    @abstractmethod
    def agent_error(self, msg: str):
        pass

    @abstractmethod
    def messages_changed(self, messages: list[api_types.SDKSessionTranscription]):
        pass


class RealtimeSession:
    def __init__(self, *, handler: RealtimeSessionHandler):
        self._microphone = VirtualMicrophone(channels=1, sample_rate=48000)
        self._audio_stream = AudioFrameStream(channels=1, sample_rate=24000)
        self._room = rtc.Room()
        self._room.on("data_received", self._on_data_received)
        self._room.on(
            "participant_metadata_changed", self._on_participant_metadata_changed
        )
        self._room.on("track_subscribed", self._on_track_subscribed)
        self._audio_source = rtc.AudioSource(sample_rate=48000, num_channels=1)
        self._handler = handler
        self._messages: list[api_types.SDKSessionTranscription] = []
        self._agent_participant: rtc.RemoteParticipant | None = None
        self._agent_audio_track: rtc.RemoteAudioTrack | None = None
        self._agent_audio_task: asyncio.Task | None = None
        self._microphone_task: asyncio.Task | None = None
        self._microphone_source = rtc.AudioSource(48000, 1)
        self._microphone_track = rtc.LocalAudioTrack.create_audio_track(
            "microphone", self._microphone_source
        )

    async def connect(self, *, opts: api_types.SDKConnectOptions):
        self._handler.connection_state_changed(api_types.SDKConnectionState.CONNECTING)
        connection_details: api_types.RealtimeSessionConnectionDetails
        if isinstance(opts.actual_instance, api_types.SDKConnectOptionsOneOf):
            connection_details = opts.actual_instance.connection_details
        elif isinstance(opts.actual_instance, api_types.SDKConnectOptionsOneOf1):
            connection_details = await self._connection_details_from_usage_token(
                usage_token=opts.actual_instance.token,
                config=opts.actual_instance.config,
            )
        else:
            raise ValueError("Invalid SDKConnectOptions type")

        try:
            await self._room.connect(
                url=connection_details.url,
                token=connection_details.token,
                options=rtc.RoomOptions(auto_subscribe=True),
            )
        except Exception as e:
            self._handler.connection_state_changed(
                api_types.SDKConnectionState.NOT_CONNECTED
            )
            logging.error(f"Failed to connect to room: {e}")
            self._handler.agent_error(str(e))

        await self._room.local_participant.publish_track(
            track=self._microphone_track,
            options=rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE),
        )
        self._microphone_task = asyncio.create_task(self._microphone_loop())

    async def disconnect(self):
        await self._room.disconnect()
        self._microphone._close()
        self._audio_stream._close()

    async def _connection_details_from_usage_token(
        self,
        *,
        usage_token: str,
        config: api_types.RealtimeSessionConfigCreate,
    ):
        api = create_api(usage_token=usage_token)
        request = api_types.StartRealtimeSessionRequest(
            config=config,
        )
        rts = await api.realtime.start_realtime_session(request)
        return rts.connection_details

    @property
    def microphone(self):
        return self._microphone

    @property
    def audio_stream(self):
        return self._audio_stream

    def _on_data_received(self, data: rtc.DataPacket):
        str_data = data.data.decode("utf-8")
        if data.topic == "message":
            t = api_types.SDKSessionTranscription.from_json(str_data)
            if t is None:
                logging.error(f"Failed to parse message: {str_data}")
                return
            self._messages.append(t)
            self._handler.messages_changed(self._messages)
        elif data.topic == "error":
            err_dict = json.loads(str_data)
            self._handler.agent_error(err_dict["message"])

    def _on_participant_metadata_changed(
        self, participant: rtc.Participant, old_metadata: str, metadata: str
    ):
        if metadata == "":
            return
        json_md = json.loads(metadata)
        if "remaining_seconds" in json_md:
            self._handler.remaining_seconds_changed(json_md["remaining_seconds"])
        if "agent_state" in json_md:
            agent_state = json_md["agent_state"]
            self._handler.agent_state_changed(api_types.SDKAgentState(agent_state))

    def _on_track_subscribed(
        self,
        track: rtc.Track,
        publication: rtc.TrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        if track.kind != rtc.TrackKind.KIND_AUDIO:
            return

        if self._agent_participant is None:
            self._agent_participant = participant

        self._agent_audio_track = cast(rtc.RemoteAudioTrack, track)
        if self._agent_audio_task is not None:
            self._agent_audio_task.cancel()

        self._agent_audio_task = asyncio.create_task(self._process_audio())
        self._handler.connection_state_changed(api_types.SDKConnectionState.CONNECTED)

    async def send_chat(self, *, text: str):
        msg_data = {"text": text}
        await self._room.local_participant.publish_data(
            payload=json.dumps(msg_data).encode("utf-8")
        )

    async def _process_audio(self):
        if self._agent_audio_track is None:
            logging.error("No audio track to process")
            return

        try:
            logging.info("Processing audio")
            stream = rtc.AudioStream(self._agent_audio_track, sample_rate=24000)
            async for frame in stream:
                self._audio_stream._push_audio(frame=bytes(frame.frame.data))
        except Exception as e:
            logging.error("Failed to process audio", exc_info=e)
            self._handler.agent_error(str(e))

    async def _microphone_loop(self):
        async for frame in self._microphone:
            try:
                f = rtc.AudioFrame(
                    data=frame,
                    sample_rate=48000,
                    num_channels=1,
                    samples_per_channel=len(frame) // 2,
                )
                logging.info(f"Microphone frame: {f}")
                await self._microphone_source.capture_frame(frame=f)
            except Exception as e:
                logging.error(f"Failed to push audio frame: {e}")


class AudioFrameStream:
    def __init__(self, *, channels: int, sample_rate: int):
        self._channels = channels
        self._sample_rate = sample_rate
        self._output_queue = asyncio.Queue[bytes | None]()

    def _close(self):
        self._output_queue.put_nowait(None)

    def _push_audio(self, *, frame: bytes):
        self._output_queue.put_nowait(frame)

    def __aiter__(self):
        return self

    async def __anext__(self):
        frame = await self._output_queue.get()
        if frame is None:
            raise StopAsyncIteration
        return frame


class VirtualMicrophone:
    def __init__(self, *, channels: int, sample_rate: int):
        self._channels = channels
        self._sample_rate = sample_rate
        self._output_queue = asyncio.Queue[bytes | None]()

    def push_audio(self, audio: bytes):
        self._output_queue.put_nowait(audio)

    def _close(self):
        self._output_queue.put_nowait(None)

    def __aiter__(self):
        return self

    async def __anext__(self):
        frame = await self._output_queue.get()
        if frame is None:
            raise StopAsyncIteration
        return frame
