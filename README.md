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

# Error 1: `bidi.BackgroundConsumer` error log on shutdown using very simple client server implementation

* `simple_api_core_repro.py`: This script contains an extremely simple ping server and client 
call using the `bidi.BidiRpc` and `bidi.BackgroundConsumer` classes which results in an error being logged.
* The error is generated every single time the client is shutdown.

```bash
pipenv run python simple_api_core_repro.py
```

Output:

```
14:38:29 - INFO - root - MainThread - Starting consumer
14:38:29 - DEBUG - google.api_core.bidi - MainThread - Started helper thread Thread-ConsumeBidirectionalStream
14:38:29 - DEBUG - root - MainThread - RPC not yet active
14:38:29 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
14:38:29 - DEBUG - root - MainThread - RPC active
14:38:29 - DEBUG - root - MainThread - Sending request
14:38:29 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - recved response.
14:38:29 - DEBUG - root - Thread-ConsumeBidirectionalStream - _on_response({'number': '1'})
14:38:29 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
14:38:29 - DEBUG - root - MainThread - Response received
14:38:29 - DEBUG - root - MainThread - Starting shutdown
14:38:29 - DEBUG - google.api_core.bidi - Thread-3 - Cleanly exiting request generator.
14:38:29 - ERROR - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream caught unexpected exception <_MultiThreadedRendezvous of RPC that terminated with:
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
14:38:29 - INFO - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream exiting
14:38:29 - DEBUG - root - MainThread - Shutdown complete
```

# Error 2: Debug level exception in `bidi.BackgroundConsumer` on shutdown when using the BigQuery Storage Write API

* The same error from above is present in logs when using clients built on top of the BidiRpc/BackgroundConsumer like the
BigQuery Storage Write API but it shows up differently. 
* Specifically, something related to how gRPC channels are created in official google clients means that the channel
gets wrapped in a `_StreamingResponseIterator` which converts the `_MultiThreadedRendezvous` into a `GoogleAPICallError` 
* This means the level is reduced to DEBUG but a stack trace is still present in the logs.

```bash
pipenv run python bq_storage_write_repro.py --project-id PROJECT_ID --dataset-id DATASET_ID --table-id test_table --create-table
```

Output:

```
...
14:41:08 - DEBUG - google.api_core.bidi - MainThread - Started helper thread Thread-ConsumeBidirectionalStream
14:41:13 - DEBUG - google.auth.transport.requests - Thread-3 - Making request: POST https://oauth2.googleapis.com/token
14:41:13 - DEBUG - urllib3.connectionpool - Thread-3 - Starting new HTTPS connection (1): oauth2.googleapis.com:443
14:41:13 - DEBUG - urllib3.connectionpool - Thread-3 - https://oauth2.googleapis.com:443 "POST /token HTTP/1.1" 200 None
14:41:14 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
14:41:14 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - recved response.
14:41:14 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - waiting for recv.
14:41:14 - DEBUG - google.cloud.bigquery_storage_v1.writer - MainThread - Stopping consumer.
14:41:14 - DEBUG - google.api_core.bidi - Thread-2 - Cleanly exiting request generator.
14:41:14 - DEBUG - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream caught error 499 Locally cancelled by application! and will exit. Generally this is due to the RPC itself being cancelled and the error will be surfaced to the calling code.
Traceback (most recent call last):
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/grpc_helpers.py", line 116, in __next__
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
  File "/Users/dhendry/code/tmp-grpc-client-and-bq-storage-write-errors-repro/.venv/lib/python3.9/site-packages/google/api_core/grpc_helpers.py", line 119, in __next__
    raise exceptions.from_grpc_error(exc) from exc
google.api_core.exceptions.Cancelled: 499 Locally cancelled by application!
14:41:14 - INFO - google.cloud.bigquery_storage_v1.writer - Thread-1 - RPC termination has signaled streaming pull manager shutdown.
14:41:14 - INFO - google.api_core.bidi - Thread-ConsumeBidirectionalStream - Thread-ConsumeBidirectionalStream exiting
14:41:14 - DEBUG - google.cloud.bigquery_storage_v1.writer - MainThread - Finished stopping manager.
14:41:14 - DEBUG - root - MainThread - Stream closed, insertion success
```

# Error 3: Uncaught exception in `bidi.BackgroundConsumer` log when using the BigQuery Storage Write API

* I have not been able to craft a reproducible example for this error, however here is the relevant stack track
which occurs in our production environment (Google AppEngine flexible) occasionally.
* It seems to be occurring along a very similar code path to the above example however the internal state of the grpc
channel seems to be a bit different and the result is an uncaught `StopIteration` exception

```
Thread-ConsumeBidirectionalStream caught unexpected exception  and will exit.
Traceback (most recent call last):
  File "/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 663, in _thread_main
    response = self._bidi_rpc.recv()
  File "/.venv/lib/python3.9/site-packages/google/api_core/bidi.py", line 346, in recv
    return next(self.call)
  File "/.venv/lib/python3.9/site-packages/google/api_core/grpc_helpers.py", line 119, in __next__
    return next(self._wrapped)
  File "/.venv/lib/python3.9/site-packages/ddtrace/contrib/grpc/client_interceptor.py", line 162, in __next__
    return self._next()
  File "/.venv/lib/python3.9/site-packages/ddtrace/contrib/grpc/client_interceptor.py", line 144, in _next
    return next(self.__wrapped__)
  File "/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 540, in __next__
    return self._next()
  File "/.venv/lib/python3.9/site-packages/grpc/_channel.py", line 964, in _next
    raise StopIteration()
StopIteration
```
