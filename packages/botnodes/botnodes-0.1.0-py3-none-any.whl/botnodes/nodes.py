from abc import abstractmethod
import json
from typing import Awaitable, Generic, Self, TypeVar, cast, Callable


from .union_serialize import Model, Serializer, UnionSerializer, End

from redis.asyncio import Redis

Context = TypeVar('Context')

Event = TypeVar('Event')
UserId = TypeVar('UserId', bound=str | int)

NodeModel = TypeVar('NodeModel', bound=Model)


class Node(Model, Generic[Context, Event, UserId, NodeModel]):
    _data: NodeModel

    @abstractmethod
    async def on_enter(self, user_id: UserId, ctx: Context) -> None:
        ...

    @abstractmethod
    async def on_event(
        self,
        user_id: UserId,
        event: Event,
        ctx: Context
    ) -> 'Node':
        ...

    @classmethod
    @abstractmethod
    def _get_model(cls) -> type[NodeModel]:
        ...

    def model_dump(self):
        return self._data.model_dump()

    @classmethod
    def model_validate(cls, obj) -> Self:
        node = super().__new__(cls)
        node._data = cls._get_model().model_validate(obj)
        return node


class Nodes(Generic[Context, Event, UserId]):
    def __init__(
        self,
        redis_client: Redis,
        redis_property_name: str,
        nodes_dict: dict[str, type[Node]],
        discriminator_field: str,
        get_start_node: Callable[[Event], Node],
        ctx: Context,
        event_to_user_id: Callable[[Event], UserId],
    ):

        self._redis_client = redis_client
        self._redis_property_name = redis_property_name
        self._serializer: Serializer[Node] = UnionSerializer(
            discriminator_field, {key: End(N) for key, N in nodes_dict.items()})
        self._get_start_node = get_start_node
        self._ctx = ctx
        self._event_to_user_id = event_to_user_id

    async def route(self, event: Event):
        user_id = self._event_to_user_id(event)

        node = await self.user(user_id).get_node()

        if node:
            next_node = await node.on_event(user_id, event, self._ctx)
        else:
            next_node = self._get_start_node(event)

        await next_node.on_enter(user_id, self._ctx)

        new_node_dict = self._serializer.serialize(next_node)
        new_json_str = json.dumps(new_node_dict)

        await cast(Awaitable[str | None], self._redis_client.hset(
            self._redis_property_name,
            str(user_id),
            new_json_str
        ))

    def user(self, user_id: UserId):
        return NodesUser(
            user_id,
            self._redis_client,
            self._redis_property_name,
            self._serializer,
            self._ctx
        )


class NodesUser(Generic[Context, Event, UserId]):
    def __init__(
        self,
        user_id: UserId,
        redis_client: Redis,
        redis_property_name: str,
        serializer: Serializer[Node],
        ctx: Context,
    ):
        self._user_id = user_id
        self._redis_client = redis_client
        self._redis_property_name = redis_property_name
        self._serializer: Serializer[Node] = serializer
        self._ctx = ctx

    async def to(self, node: Node):
        await node.on_enter(self._user_id, self._ctx)

        node_dict = self._serializer.serialize(node)
        json_str = json.dumps(node_dict)

        await cast(Awaitable[str | None], self._redis_client.hset(
            self._redis_property_name,
            str(self._user_id),
            json_str
        ))

    async def get_node(self):
        json_str = await cast(Awaitable[str | None], self._redis_client.hget(
            self._redis_property_name,
            str(self._user_id)
        ))

        if json_str:
            dict = json.loads(json_str)
            node = self._serializer.deserialize(dict)
            return node
