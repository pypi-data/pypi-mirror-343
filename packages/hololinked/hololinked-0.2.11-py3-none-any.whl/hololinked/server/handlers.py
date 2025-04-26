import asyncio
import zmq.asyncio
import typing
import uuid
from tornado.web import RequestHandler, StaticFileHandler
from tornado.iostream import StreamClosedError


from .dataklasses import HTTPResource, ServerSentEvent
from .utils import *
from .zmq_message_brokers import AsyncEventConsumer, EventConsumer
from .schema_validators import BaseSchemaValidator


class BaseHandler(RequestHandler):
    """
    Base request handler for RPC operations
    """

    def initialize(self, resource : typing.Union[HTTPResource, ServerSentEvent], validator : BaseSchemaValidator, 
                            owner = None) -> None:
        """
        Parameters
        ----------
        resource: HTTPResource | ServerSentEvent
            resource representation of Thing's exposed object using a dataclass
        owner: HTTPServer
            owner ``hololinked.server.HTTPServer.HTTPServer`` instance
        """
        from .HTTPServer import HTTPServer
        assert isinstance(owner, HTTPServer)
        self.resource = resource
        self.schema_validator = validator
        self.owner = owner
        self.zmq_client_pool = self.owner.zmq_client_pool 
        self.serializer = self.owner.serializer
        self.logger = self.owner.logger
        self.allowed_clients = self.owner.allowed_clients
       
    def set_headers(self) -> None:
        """
        override this to set custom headers without having to reimplement entire handler
        """
        raise NotImplementedError("implement set headers in child class to automatically call it" +
                            " after directing the request to Thing")
    
    def get_execution_parameters(self) -> typing.Tuple[typing.Dict[str, typing.Any], 
                                                typing.Dict[str, typing.Any], typing.Union[float, int, None]]:
        """
        merges all arguments to a single JSON body and retrieves execution context (like oneway calls, fetching executing
        logs) and timeouts
        """
        if len(self.request.body) > 0:
            arguments = self.serializer.loads(self.request.body)
        else:
            arguments = dict()
        if isinstance(arguments, dict):
            if len(self.request.query_arguments) >= 1:
                for key, value in self.request.query_arguments.items():
                    if len(value) == 1:
                        arguments[key] = self.serializer.loads(value[0]) 
                    else:
                        arguments[key] = [self.serializer.loads(val) for val in value]
            context = dict(fetch_execution_logs=arguments.pop('fetch_execution_logs', False))
            timeout = arguments.pop('timeout', None)
            if timeout is not None and timeout < 0:
                timeout = None
            if self.resource.request_as_argument:
                arguments['request'] = self.request
            return arguments, context, timeout
        return arguments, dict(), 5 # arguments, context is empty, 5 seconds invokation timeout, hardcoded needs to be fixed
    
    @property
    def has_access_control(self) -> bool:
        """
        Checks if a client is an allowed client. Requests from un-allowed clients are reject without execution. Custom
        web handlers can use this property to check if a client has access control on the server or ``Thing``.
        """
        if len(self.allowed_clients) == 0:
            self.set_header("Access-Control-Allow-Origin", "*")
            return True
        # For credential login, access control allow origin cannot be '*',
        # See: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#examples_of_access_control_scenarios
        origin = self.request.headers.get("Origin")
        if origin is not None and (origin in self.allowed_clients or origin + '/' in self.allowed_clients):
            self.set_header("Access-Control-Allow-Origin", origin)
            return True
        return False
    
    def set_access_control_allow_headers(self) -> None:
        """
        For credential login, access control allow headers cannot be a wildcard '*'. 
        Some requests require exact list of allowed headers for the client to access the response. 
        Use this method in set_headers() override if necessary. 
        """
        headers = ", ".join(self.request.headers.keys())
        if self.request.headers.get("Access-Control-Request-Headers", None):
            headers += ", " + self.request.headers["Access-Control-Request-Headers"]
        self.set_header("Access-Control-Allow-Headers", headers)



class RPCHandler(BaseHandler):
    """
    Handler for property read-write and method calls
    """

    async def get(self) -> None:
        """
        runs property or action if accessible by 'GET' method. Default for property reads. 
        """
        await self.handle_through_thing('GET')    

    async def post(self) -> None:
        """
        runs property or action if accessible by 'POST' method. Default for action execution.
        """
        await self.handle_through_thing('POST')
    
    async def patch(self) -> None:
        """
        runs property or action if accessible by 'PATCH' method.
        """
        await self.handle_through_thing('PATCH')        
    
    async def put(self) -> None:
        """
        runs property or action if accessible by 'PUT' method. Default for property writes.
        """
        await self.handle_through_thing('PUT')        
    
    async def delete(self) -> None:
        """
        runs property or action if accessible by 'DELETE' method. Default for property deletes. 
        """
        await self.handle_through_thing('DELETE')  
       
    def set_headers(self) -> None:
        """
        sets default headers for RPC (property read-write and action execution). The general headers are listed as follows:

        .. code-block:: yaml 

            Content-Type: application/json
            Access-Control-Allow-Credentials: true
            Access-Control-Allow-Origin: <client>
        """
        self.set_header("Content-Type" , "application/json")    
        self.set_header("Access-Control-Allow-Credentials", "true")
    
    async def options(self) -> None:
        """
        Options for the resource. Main functionality is to inform the client is a specific HTTP method is supported by 
        the property or the action (Access-Control-Allow-Methods).
        """
        if self.has_access_control:
            self.set_status(204)
            self.set_access_control_allow_headers()
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Methods", ', '.join(self.resource.instructions.supported_methods()))
        else:
            self.set_status(401, "forbidden")
        self.finish()
    

    async def handle_through_thing(self, http_method : str) -> None:
        """
        handles the actual RPC call, called by each of the HTTP methods with their name as the argument. 
        """
        if not self.has_access_control:
            self.set_status(401, "forbidden")    
        elif http_method not in self.resource.instructions:
            self.set_status(404, "not found")
        else:
            reply = None
            try:
                arguments, context, timeout = self.get_execution_parameters()
                if self.schema_validator is not None:
                    self.schema_validator.validate(arguments)
                reply = await self.zmq_client_pool.async_execute(
                                        instance_name=self.resource.instance_name, 
                                        instruction=self.resource.instructions.__dict__[http_method], 
                                        arguments=arguments,
                                        context=context, 
                                        raise_client_side_exception=False, 
                                        invokation_timeout=timeout, 
                                        execution_timeout=None, 
                                        argument_schema=self.resource.argument_schema
                                    ) # type: ignore
                # message mapped client pool currently strips the data part from return message
                # and provides that as reply directly 
                self.set_status(200, "ok")
            except ConnectionAbortedError as ex:
                self.set_status(503, str(ex))
                event_loop = asyncio.get_event_loop()
                event_loop.call_soon(lambda : asyncio.create_task(self.owner.update_router_with_thing(
                                                                    self.zmq_client_pool[self.resource.instance_name])))
            except ConnectionError as ex:
                await self.owner.update_router_with_thing(self.zmq_client_pool[self.resource.instance_name])
                await self.handle_through_thing(http_method) # reschedule
                return 
            except Exception as ex:
                self.logger.error(f"error while scheduling RPC call - {str(ex)}")
                self.logger.debug(f"traceback - {ex.__traceback__}")
                self.set_status(500, "error while scheduling RPC call")
                reply = self.serializer.dumps({"exception" : format_exception_as_json(ex)})
            self.set_headers()
            if reply:
                self.write(reply)
        self.finish()
        
    
        
class EventHandler(BaseHandler):
    """
    handles events emitted by ``Thing`` and tunnels them as HTTP SSE. 
    """
    def initialize(self, resource, validator: BaseSchemaValidator, owner=None) -> None:
        super().initialize(resource, validator, owner)
        self.data_header = b'data: %s\n\n'

    def set_headers(self) -> None:
        """
        sets default headers for event handling. The general headers are listed as follows:

        .. code-block:: yaml 

            Content-Type: text/event-stream
            Cache-Control: no-cache
            Connection: keep-alive
            Access-Control-Allow-Credentials: true
            Access-Control-Allow-Origin: <client>
        """
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        self.set_header("Access-Control-Allow-Credentials", "true")

    async def get(self):
        """
        events are support only with GET method.
        """
        if self.has_access_control:
            self.set_headers()
            await self.handle_datastream()
        else:
            self.set_status(401, "forbidden")
        self.finish()

    async def options(self):
        """
        options for the resource.
        """
        if self.has_access_control:
            self.set_status(204)
            self.set_access_control_allow_headers()
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Methods", 'GET')
        else:
            self.set_status(401, "forbidden")
        self.finish()

    def receive_blocking_event(self, event_consumer : EventConsumer):
        return event_consumer.receive(timeout=10000, deserialize=False)

    async def handle_datastream(self) -> None:    
        """
        called by GET method and handles the event.
        """
        try:                        
            event_consumer_cls = EventConsumer if self.owner._zmq_inproc_event_context else AsyncEventConsumer
            # synchronous context with INPROC pub or asynchronous context with IPC or TCP pub, we handle both in async 
            # fashion as HTTP server should be running purely sync(or normal) python method.
            event_consumer = event_consumer_cls(self.resource.unique_identifier, self.resource.socket_address, 
                                            identity=f"{self.resource.unique_identifier}|HTTPEvent|{uuid.uuid4()}",
                                            logger=self.logger, http_serializer=self.serializer, 
                                            context=self.owner._zmq_inproc_event_context if self.resource.socket_address.startswith('inproc') else None)
            event_loop = asyncio.get_event_loop()
            self.set_status(200)
        except Exception as ex:
            self.logger.error(f"error while subscribing to event - {str(ex)}")
            self.set_status(500, "could not subscribe to event source from thing")
            self.write(self.serializer.dumps({"exception" : format_exception_as_json(ex)}))
            return
        
        while True:
            try:
                if isinstance(event_consumer, AsyncEventConsumer):
                    data = await event_consumer.receive(timeout=10000, deserialize=False)
                else:
                    data = await event_loop.run_in_executor(None, self.receive_blocking_event, event_consumer)
                if data:
                    # already JSON serialized 
                    self.write(self.data_header % data)
                    await self.flush() # log after flushing just to be sure
                    self.logger.debug(f"new data sent - {self.resource.name}")
                else:
                    self.logger.debug(f"found no new data - {self.resource.name}")
                    await self.flush() # heartbeat - raises StreamClosedError if client disconnects
            except StreamClosedError:
                break 
            except Exception as ex:
                self.logger.error(f"error while pushing event - {str(ex)}")
                self.write(self.data_header % self.serializer.dumps(
                    {"exception" : format_exception_as_json(ex)}))
        try:
            if isinstance(self.owner._zmq_inproc_event_context, zmq.asyncio.Context):
                event_consumer.exit()
        except Exception as ex:
            self.logger.error(f"error while closing event consumer - {str(ex)}" )


class JPEGImageEventHandler(EventHandler):
    """
    handles events with images with image data header
    """
    def initialize(self, resource, validator: BaseSchemaValidator, owner = None) -> None:
        super().initialize(resource, validator, owner)
        self.data_header = b'data:image/jpeg;base64,%s\n\n'


class PNGImageEventHandler(EventHandler):
    """
    handles events with images with image data header
    """
    def initialize(self, resource, validator: BaseSchemaValidator, owner = None) -> None:
        super().initialize(resource, validator, owner)
        self.data_header = b'data:image/png;base64,%s\n\n'
    


class FileHandler(StaticFileHandler):

    @classmethod
    def get_absolute_path(cls, root: str, path: str) -> str:
        """
        Returns the absolute location of ``path`` relative to ``root``.

        ``root`` is the path configured for this `StaticFileHandler`
        (in most cases the ``static_path`` `Application` setting).

        This class method may be overridden in subclasses.  By default
        it returns a filesystem path, but other strings may be used
        as long as they are unique and understood by the subclass's
        overridden `get_content`.

        .. versionadded:: 3.1
        """
        return root+path
    


class ThingsHandler(BaseHandler):
    """
    add or remove things
    """

    async def get(self):
        self.set_status(404)
        self.finish()
    
    async def post(self):
        if not self.has_access_control:
            self.set_status(401, 'forbidden')
        else:
            try:
                instance_name = ""
                await self.zmq_client_pool.create_new(server_instance_name=instance_name)
                await self.owner.update_router_with_thing(self.zmq_client_pool[instance_name])
                self.set_status(204, "ok")
            except Exception as ex:
                self.set_status(500, str(ex))
            self.set_headers()
        self.finish()

    async def options(self):
        if self.has_access_control:
            self.set_status(204)
            self.set_access_control_allow_headers()
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header("Access-Control-Allow-Methods", 'GET, POST')
        else:
            self.set_status(401, "forbidden")
        self.finish()


class StopHandler(BaseHandler):
    """Stops the tornado HTTP server"""

    def initialize(self, owner = None) -> None:
        from .HTTPServer import HTTPServer
        assert isinstance(owner, HTTPServer)
        self.owner = owner    
        self.allowed_clients = self.owner.allowed_clients
    
    async def post(self):
        if not self.has_access_control:
            self.set_status(401, 'forbidden')
        else:
            try:
                # Stop the Tornado server
                asyncio.get_event_loop().call_soon(lambda : asyncio.create_task(self.owner.stop()))
                self.set_status(204, "ok")
                self.set_header("Access-Control-Allow-Credentials", "true")
            except Exception as ex:
                self.set_status(500, str(ex))
        self.finish()