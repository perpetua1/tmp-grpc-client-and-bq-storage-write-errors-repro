# tmp-grpc-client-and-bq-storage-write-errors-repro

Please note this is a public repo. 

This repo contains code to reproduces errors we have encountered with the python grpc client and bigquery 
storage write API.

# Setup

```bash
pipenv install
```

OR, if you dont want to use pipenv:

```bash
pip install -r requirements.txt
```

# Error: `bidi.BackgroundConsumer` error log on shutdown

## Repro:

```bash
pipenv run python simple_api_core_repro.py
```

* This script contains an extremely simple ping server and test client code
* We simply create a BidiRpc and BackgroundConsumer, send one message, then shut it down

## Output:

```
2024-02-02 12:54:30,708 - INFO - root - MainThread - Starting consumer
2024-02-02 12:54:30,708 - DEBUG - google.api_core.bidi - MainThread - Started helper thread Thread-ConsumeBidirectionalStream
2024-02-02 12:54:30,708 - DEBUG - root - MainThread - RPC not yet active
2024-02-02 12:54:30,708 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
2024-02-02 12:54:30,714 - DEBUG - root - MainThread - RPC active
2024-02-02 12:54:30,714 - DEBUG - root - MainThread - Sending request
2024-02-02 12:54:30,715 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - recved response.
2024-02-02 12:54:30,715 - DEBUG - root - Thread-ConsumeBidirectionalStream - _on_response({'number': '1'})
2024-02-02 12:54:30,715 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
2024-02-02 12:54:30,715 - DEBUG - root - MainThread - Response received
2024-02-02 12:54:30,715 - DEBUG - root - MainThread - Starting shutdown
2024-02-02 12:54:30,716 - DEBUG - google.api_core.bidi - Thread-3 - Cleanly exiting request generator.
2024-02-02 12:54:30,716 - ERROR - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream caught unexpected exception <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.CANCELLED
	details = "Locally cancelled by application!"
	debug_error_string = "None"
> and will exit.
Traceback (most recent call last):
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 663, in _thread_main
    response = self._bidi_rpc.recv()
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 346, in recv
    return next(self.call)
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 540, in __next__
    return self._next()
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 966, in _next
    raise self
grpc._channel._MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.CANCELLED
	details = "Locally cancelled by application!"
	debug_error_string = "None"
>
2024-02-02 12:54:30,717 - INFO - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream exiting
2024-02-02 12:54:30,717 - DEBUG - root - MainThread - Shutdown complete
```