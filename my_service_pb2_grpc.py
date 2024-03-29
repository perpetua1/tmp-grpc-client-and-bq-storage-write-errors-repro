# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import my_service_pb2 as my__service__pb2


class MyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PingStream = channel.stream_stream(
                '/my_service.MyService/PingStream',
                request_serializer=my__service__pb2.PingRequest.SerializeToString,
                response_deserializer=my__service__pb2.PingResponse.FromString,
                )


class MyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PingStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PingStream': grpc.stream_stream_rpc_method_handler(
                    servicer.PingStream,
                    request_deserializer=my__service__pb2.PingRequest.FromString,
                    response_serializer=my__service__pb2.PingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'my_service.MyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PingStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/my_service.MyService/PingStream',
            my__service__pb2.PingRequest.SerializeToString,
            my__service__pb2.PingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
