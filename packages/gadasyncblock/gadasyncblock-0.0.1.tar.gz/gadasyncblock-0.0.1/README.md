<p align="center">
  <a href="https://github.com/AlexDemure/gadasyncblock">
    <a href="https://ibb.co/4gMDDpK7"><img src="https://i.ibb.co/JF2bbHmK/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  Event loop lock detector for Python.
</p>

---

### Installation

```
pip install gadasyncblock
```

### Usage

```python
import contextlib

from fastapi import FastAPI

from gadasyncblock import AsyncBlock

detector = AsyncBlock(timeout=1)

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    await detector.start()
    yield
    await detector.shutdown()


app = FastAPI(lifespan=lifespan)

@app.post("/run")
async def run():
    time.sleep(2)
    return {"message": "Blocked"}
```
