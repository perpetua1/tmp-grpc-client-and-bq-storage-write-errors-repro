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

# Error 1) `bidi.BackgroundConsumer` error log on shutdown using very simple client server implementation

* `simple_api_core_repro.py`: This script contains an extremely simple ping server and client 
call using the `bidi.BidiRpc` and `bidi.BackgroundConsumer` classes which results in an error being logged.
* The error is generated every single time the client is shutdown.

```bash
pipenv run python simple_api_core_repro.py
```

Output:

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

# Error 1.b) `bidi.BackgroundConsumer` log when using the BigQuery Storage Write API

* The same error from above is present in logs when using clients built on top of the BidiRpc/BackgroundConsumer like the
BigQuery Storage Write API but it shows up differently. 
* Specifically, something related to how gRPC channels are created in official google clients means that the channel
gets wrapped in a `_StreamingResponseIterator` which converts the `_MultiThreadedRendezvous` into a `GoogleAPICallError` 


```bash
pipenv run python simple_api_core_repro.py
```

Output:

```
...
2024-02-02 14:02:39,816 - DEBUG - google.api_core.bidi - MainThread - Started helper thread Thread-ConsumeBidirectionalStream
2024-02-02 14:02:44,903 - DEBUG - google.auth.transport.requests - Thread-3 - Making request: POST https://oauth2.googleapis.com/token
2024-02-02 14:02:44,907 - DEBUG - urllib3.connectionpool - Thread-3 - Starting new HTTPS connection (1): oauth2.googleapis.com:443
2024-02-02 14:02:45,051 - DEBUG - urllib3.connectionpool - Thread-3 - https://oauth2.googleapis.com:443 "POST /token HTTP/1.1" 200 None
2024-02-02 14:02:45,460 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
2024-02-02 14:02:45,460 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - recved response.
2024-02-02 14:02:45,460 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
2024-02-02 14:02:45,492 - DEBUG - google.cloud.bigquery_storage_v1.writer - MainThread - Stopping consumer.
2024-02-02 14:02:45,495 - DEBUG - google.api_core.bidi - Thread-2 - Cleanly exiting request generator.
2024-02-02 14:02:45,495 - INFO - google.cloud.bigquery_storage_v1.writer - Thread-1 - RPC termination has signaled streaming pull manager shutdown.
2024-02-02 14:02:45,497 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream caught error 499 Locally cancelled by application! and will exit. Generally this is due to the RPC itself being cancelled and the error will be surfaced to the calling code.
Traceback (most recent call last):
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/grpc_helpers.py", line 119, in __next__
    return next(self._wrapped)
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 540, in __next__
    return self._next()
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 966, in _next
    raise self
grpc._channel._MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.CANCELLED
	details = "Locally cancelled by application!"
	debug_error_string = "None"
>

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 663, in _thread_main
    response = self._bidi_rpc.recv()
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 346, in recv
    return next(self.call)
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/grpc_helpers.py", line 122, in __next__
    raise exceptions.from_grpc_error(exc) from exc
google.api_core.exceptions.Cancelled: 499 Locally cancelled by application!
2024-02-02 14:02:45,510 - INFO - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream exiting
2024-02-02 14:02:45,512 - DEBUG - google.cloud.bigquery_storage_v1.writer - MainThread - Finished stopping manager.
2024-02-02 14:02:45,512 - DEBUG - root - MainThread - Stream closed, insertion success
```

