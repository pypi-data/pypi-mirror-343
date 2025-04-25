# lcmutils

Python utility library for Lightweight Communications and Marshalling (LCM).

## Installation

```bash
pip install lcmutils
```

## Usage

### Typing

`lcmutils` defines the `LCMType` protocol for LCM type classes generated via `lcm-gen`. You can use this protocol to type hint LCM type classes in your Python code.

```python
from lcmutils import LCMType

def publish_lcm_message(lcm: LCM, message: LCMType) -> None:
    lcm.publish("channel", message.encode())
```

### LCM Daemon

For many applications, it's desirable to run LCM handling in a background thread. `lcmutils` provides a `LCMDaemon` class that wraps an `LCM` instance and repeatedly calls its the `handle` method in a background thread.

```python
from lcmutils import LCMDaemon

lcm = LCMDaemon()

@lcm.subscribe("channel1", "channel2")
def handle_message(channel: str, data: bytes) -> None:
    print(f"Received message {data} on channel {channel}")

lcm.start()
...
lcm.stop()  # will stop when the next message is handled
```

By default, the `LCMDaemon` instance will use the blocking `LCM.handle` method. If you want to use the `LCM.handle_timeout` method instead, you can pass a `timeout_millis` argument to the constructor. You can also pass a `start` argument to automatically start the daemon.

```python
from lcmutils import LCMDaemon

# Use LCM.handle_timeout with a 100ms timeout and start the daemon
lcm = LCMDaemon(timeout_millis=100, start=True)
...
lcm.stop()  # will stop within 100ms
```

`LCMDaemon` can be passed an existing `LCM` instance to wrap, or it will create a new `LCM` instance if none is provided.

```python
from lcm import LCM
from lcmutils import LCMDaemon

lcm = LCM("udpm://239.255.76.67:7667?ttl=1")  # create an LCM instance with ttl=1
lcm_daemon = LCMDaemon(lcm, start=True)
...
lcm_daemon.stop()
```

### Type Registry

`lcmutils` provides an `LCMTypeRegistry` class that can be used to register and lookup LCM type classes by fingerprint.

```python
from lcmutils import LCMTypeRegistry
from my_lcm_types import MyLCMType

registry = LCMTypeRegistry(MyLCMType)
# or:
#   registry = LCMTypeRegistry()
#   registry.register(MyLCMType)

msg = MyLCMType()
msg_encoded = msg.encode()

print(registry.detect(msg_encoded))         # MyLCMType
print(registry.decode(msg_encoded) == msg)  # True
```
