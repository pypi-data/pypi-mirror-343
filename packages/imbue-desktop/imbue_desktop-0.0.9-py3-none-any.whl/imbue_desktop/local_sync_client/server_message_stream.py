from typing import AsyncGenerator
from typing import Protocol
from typing import Self
from typing import TypeVar

from imbue_core.cattrs_serialization import deserialize_from_json
from imbue_core.local_sync import LocalSyncServerMessage
from imbue_desktop.errors import StreamCloseError
from imbue_desktop.local_sync_client.constants import MAX_MESSAGE_STREAM_CHUNK_SIZE

T = TypeVar("T")


class AsyncStreamIterator(Protocol[T]):
    def __aiter__(self) -> Self:
        ...

    async def __anext__(self) -> T:
        ...


class AsyncStreamReader(Protocol):
    def __aiter__(self) -> AsyncStreamIterator[bytes]:
        ...

    def iter_chunked(self, n: int) -> AsyncStreamIterator[bytes]:
        """Returns an asynchronous iterator that yields chunks of size n."""


def _get_data_from_line(line: bytes) -> LocalSyncServerMessage | None:
    if not line:
        return None
    data = line.decode("utf-8").split(": ", maxsplit=1)[-1].strip()
    if data == "null":
        raise StreamCloseError("Not expecting this stream to close...")
    if data != "":
        return deserialize_from_json(data)
    return None


class ServerMessageStream:
    def __init__(
        self,
        stream_reader: AsyncStreamReader,
        max_chunk_size: int = MAX_MESSAGE_STREAM_CHUNK_SIZE,
    ) -> None:
        self.stream_reader = stream_reader
        self.content_iterator = aiter(stream_reader)
        self.max_chunk_size = max_chunk_size

    async def _inner_iterator(self) -> AsyncGenerator[LocalSyncServerMessage, None]:
        # handle larger than expected chunk sizes
        buffer = b""
        async for chunk in self.stream_reader.iter_chunked(self.max_chunk_size):
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                data = _get_data_from_line(line)
                if data is not None:
                    yield data

        if buffer:
            data = _get_data_from_line(buffer)
            if data is not None:
                yield data

    async def __aiter__(self) -> AsyncGenerator[LocalSyncServerMessage, None]:
        try:
            async for message in self._inner_iterator():
                yield message
        except Exception as e:
            raise StreamCloseError(f"Stream closed unexpectedly due to following exception: {str(e)}") from e

    async def __anext__(self) -> LocalSyncServerMessage:
        return await self.__aiter__().__anext__()
