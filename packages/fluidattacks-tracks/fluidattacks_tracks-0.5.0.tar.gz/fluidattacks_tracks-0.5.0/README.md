# fluidattacks-tracks

[![PyPI version](https://img.shields.io/pypi/v/fluidattacks-tracks.svg)](https://pypi.org/project/fluidattacks-tracks/)

<p align="center">
  <a href="https://fluidattacks.com/" rel="noopener" target="_blank">
  <img width="460px" src="https://res.cloudinary.com/fluid-attacks/image/upload/v1728418266/airs/logo/logo_full.png" alt="Fluid Attacks logo">
  </a>
</p>

This library provides convenient access to the Tracks API from any Python 3.11+
application. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Usage

```python
from datetime import datetime, UTC
from fluidattacks_tracks import Tracks
from fluidattacks_tracks.resources.event import Event

client = Tracks()
client.event.create(
    Event(
        action="CREATE",
        author="author",
        date=datetime.now(UTC),
        mechanism="API",
        metadata={"foo": "bar"},
        object="object",
        object_id="object_id",
    )
)
```

## Async usage

Simply import `AsyncTracks` instead of `Tracks` and use `await` with each API call:

```python
import asyncio
from datetime import datetime, UTC
from fluidattacks_tracks import Tracks
from fluidattacks_tracks.resources.event import Event

client = AsyncTracks()


async def main() -> None:
    await client.event.create(
        Event(
            action="CREATE",
            author="author",
            date=datetime.now(UTC),
            mechanism="API",
            metadata={"foo": "bar"},
            object="object",
            object_id="object_id",
        )
    )


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.
