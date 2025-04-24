from typing import List
from typing import Self

import pytest

from imbue_core.cattrs_serialization import serialize_to_json
from imbue_core.local_sync import NewRemoteRepoStateMessage
from imbue_core.repo_state import CleanRepoOperation
from imbue_desktop.local_sync_client.server_message_stream import AsyncStreamReader
from imbue_desktop.local_sync_client.server_message_stream import ServerMessageStream


class MockAsyncStreamIterator:
    def __init__(self, data_chunks: List[bytes], max_chunk_size: int) -> None:
        self.data_chunks = data_chunks
        self.index = 0
        self.max_chunk_size = max_chunk_size

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> bytes:
        if self.index < len(self.data_chunks):
            chunk = self.data_chunks[self.index]
            if len(chunk) > self.max_chunk_size:
                raise ValueError("Chunk too big")
            self.index += 1
            return chunk
        raise StopAsyncIteration


class MockAsyncStreamReader(AsyncStreamReader):
    def __init__(self, data_chunks: List[bytes], max_chunk_size: int) -> None:
        self.data_chunks = data_chunks
        self.max_chunk_size = max_chunk_size

    def __aiter__(self) -> MockAsyncStreamIterator:
        return MockAsyncStreamIterator(self.data_chunks, self.max_chunk_size)

    def iter_chunked(self, n: int) -> MockAsyncStreamIterator:
        new_chunks = []
        for chunk in self.data_chunks:
            while len(chunk) > n:
                new_chunks.append(chunk[:n])
                chunk = chunk[n:]
            if chunk:
                new_chunks.append(chunk)

        return MockAsyncStreamIterator(new_chunks, self.max_chunk_size)


@pytest.fixture
def chunk_size_() -> int:
    return 100


@pytest.fixture
def stream_reader_(chunk_size_) -> MockAsyncStreamReader:
    data = (
        b"data: "
        + serialize_to_json(
            NewRemoteRepoStateMessage(
                branch_name="test_branch",
                version=1,
                commit_hash="test_commit_hash",
                repo_operation=CleanRepoOperation(
                    combined_diff="X" * 2**16,
                    staged_diff="X" * 2**16,
                    unstaged_diff="",
                ),
            )
        ).encode("utf-8")
        + b"\n"
    )

    return MockAsyncStreamReader(data_chunks=[data], max_chunk_size=chunk_size_)


@pytest.mark.asyncio
async def test_message_with_large_chunk_size(stream_reader_, chunk_size_) -> None:
    server_message_stream = ServerMessageStream(stream_reader_, chunk_size_)
    async for message in server_message_stream:
        assert message
        assert isinstance(message, NewRemoteRepoStateMessage)
        assert message.branch_name == "test_branch"
        assert message.version == 1
        assert message.repo_operation.combined_diff == "X" * 2**16
