# `botnodes` – async user state for bots (with Redis)

A tiny helper for building bots (Telegram, Discord, etc.) that need to track **user state** between messages — in a flexible and persistent way.

Each user is placed on a **Node** – a small async class that defines:

- what happens when a user _enters_ the node
- how the node _handles incoming events_ (e.g., messages)
- what the _next node_ should be
- what _data_ is stored while the user is on the node

---

## Installation

```bash
pip install botnodes
```

---

## Basic Usage

### 1. Define a context (`Ctx`) shared across nodes

```python
# nodes_types.py
from dataclasses import dataclass
import aiogram # Assuming using aiogram as the bot library

...

@dataclass
class Ctx:
    bot: aiogram.Bot   # Assuming using aiogram as the bot library
    some_config: str
    food_api: FoodAPI  # some external service
    logger: Logger     # some logger class
```

---

### 2. Define the `Event` and `UserId` types of your bot's library, and a function to extract the user ID

```python
# nodes_types.py
from aiogram.types import Message # Assuming using aiogram as the bot library

...

Event = Message
UserId = int  # BigInt

event_to_user_id = lambda event: event.from_user.id
```

---

### 3. Define a starting node

```python
# nodes/Start.py
from pydantic import BaseModel
from botnodes import Node
from ..nodes_types import Ctx, Event, UserId

class StartModel(BaseModel):
    ...

class Start(Node[Ctx, Event, UserId, StartModel]):
    # Should always return the model, that is expected to be stored in Redis for the node
    @classmethod
    def _get_model(cls):
        return StartModel

    # Not required to be saved during node's lifetime
    # (between on_enter and on_event calls)
    # therefore outside StartModel
    _username: str
    _is_first_launch: bool

    def __init__(self, username: str, is_first_launch: bool = False):
        self._data = StartModel()
        self._username = username
        self._is_first_launch = is_first_launch

    async def on_enter(self, user_id, ctx):
        if self._is_first_launch:
            await ctx.bot.send_message(user_id, f"Hello, {self._username}! Are you hungry?") # Your bot library call
        else:
            await ctx.bot.send_message(user_id, f"Again main menu! Are you hungry?") # Your bot library call

    async def on_event(self, user_id, message, ctx):
        # Imports inside the function to avoid circular imports
        from nodes.Hungry import Hungry
        from nodes.Hold import Hold

        if message.text == 'Yes': # Your bot library's event's stucture
            await ctx.bot.send_message(user_id, 'No worries, I\'ve got you back!') # Your bot library call
            return Hungry() # Move to Hungry node
        elif message.text == 'No': # Your bot library's event's stucture
            await ctx.bot.send_message(user_id, 'Write me when you are ready then!') # Your bot library call
            return Hold() # Move to Hold node

        else:
            await ctx.bot.send_message(user_id, 'Say what?') # Your bot library call
            return Start(message.from_user.username) # Unrecognized command — stay in the main menu
```

---

### 4. Define the function that provides the starting node for a user

```python
# main.py
from nodes.Start import Start

...

def get_start_node(message: Event):
    return Start(message.from_user.username or message.from_user.full_name, True)
```

---

### 5. Define other nodes like `Hungry`

```python
# nodes/Hungry.py
from pydantic import BaseModel
from botnodes import Node
from ..nodes_types import Ctx, Event, UserId

class HungryModel(BaseModel):
    order: list[str] # We will store the active order, while the user continues choosing

class Hungry(Node[Ctx, Event, UserId, HungryModel]):
    # Should always return the model, that is expected to be stored in Redis for the node
    @classmethod
    def _get_model(cls):
        return HungryModel

    def __init__(self, order: list[str] | None = None):
        self._data = HungryModel(order=order if order else [])

    async def on_enter(self, user_id, ctx):
        cart_string = ', '.join(self._data.order) if self._data.order else 'Empty'

        # Your bot library call
        await ctx.bot.send_message(
            user_id,
            f"What are you gonna order? Cart: {cart_string}"
            )

    async def on_event(self, user_id, message, ctx):
        # Imports inside the function to avoid circular imports
        from nodes.Start import Start

        if message.text == 'Finish': # Your bot library's event's stucture
            if (not self._data.order):
                await ctx.bot.send_message(
                  user_id,
                  'Cart is empty! Write Cancel to cancel the order'
                  ) # Your bot library call
                return Hungry([])
            else:
                cart_string = ', '.join(self._data.order)
                await ctx.bot.send_message(user_id, f'Ordering {cart_string}') # Your bot library call
                try:
                    await ctx.food_api.order_food(self._data.order) # Some food api call
                    await ctx.bot.send_message(user_id, f'Ordered!') # Your bot library call
                except Exception as e:
                    ctx.logger.error(f'Order for {user_id} failed due to {e} | {self._data.order=}')
                    await ctx.bot.send_message(user_id, f'Error') # Your bot library call
                return Start(message.from_user.username) # Back to main menu

        if message.text == 'Cancel':
            await ctx.bot.send_message(user_id, f'Order cancelled!') # Your bot library call
            return Start(message.from_user.username) # Back to main menu

        else:
            new_item = message.text # Your bot library's event's stucture
            await ctx.bot.send_message(user_id, f'Added {message.text}') # Your bot library call
            return Hungry(order=[*self._data.order, new_item])
```

---

### 6. Define the `Hold` node

```python
# nodes/Hold.py
from pydantic import BaseModel
from botnodes import Node
from ..nodes_types import Ctx, Event, UserId

class HoldModel(BaseModel):
    ...

class Hold(Node[Ctx, Event, UserId, HoldModel]):
    def __init__(self):
        self._data = HoldModel()

    # Should always return the model, that is expected to be stored in Redis for the node
    @classmethod
    def _get_model(cls):
        return HoldModel

    async def on_enter(self, *_):
        pass # We are on hold — no action required

    async def on_event(self, user_id, message, ctx):
        from nodes.Start import Start
        return Start(message.from_user.username) # Return to main menu as soon as a new event from the user is recieved

```

---

### 7. Register all nodes using unique keys (not to be changed because app's state saved in Redis relies on them)

```python
# main.py

...

nodes_dict = {
  'start': Start,
  'hungry': Hungry,
  'hold': Hold
}
```

---

### 8. Set up Redis and define a property key to store state

```python
# main.py
from redis.asyncio import Redis

...
redis_property_name = 'nodes_state'

async def main():
    redis = Redis()

```

---

### 9. Initialize the `Nodes` manager

```python
# main.py
from nodes_types import Ctx

import aiogram # Assuming using aiogram as the bot library

...

async def main():
    # previous code...

    bot = aiogram.Bot(bot_token)
    some_config = 'hello world'
    food_api = ...
    logger = ...

    ctx = Ctx(bot, some_config, food_api, logger)

    nodes = Nodes(
      redis_client=redis,
      redis_property_name="mybot_state",
      nodes_dict=nodes_dict,
      discriminator_field="node_name", # Must not be in any nodes' model to avoid name conflicts
      get_start_node=get_start_node,
      ctx=ctx,
      event_to_user_id=event_to_user_id
    )
```

---

### 10. Route events using your `nodes` instance

```python
# main.py
from aiogram.types import Message
from aiogram.filters import BaseFilter

...

class IsPrivateChatMessage(BaseFilter):
    async def __call__(self, event: Message) -> bool:
        return event.chat.type == "private"

async def main():
    # previous code...

    dp = aiogram.Dispatcher() # Assuming using aiogram as the bot library

    default_router = ... # Create a router for default things, accesible from any state — if you need

    personal_router = aiogram.Router()
    personal_router.message.filter(IsPrivateChatMessage())
    personal_router.include_router(default_router)

    nodes_router = aiogram.Router()

    nodes_router.message()(nodes.route)
    personal_router.include_router(nodes_router)

    dp.include_router(personal_router)

    await dp.start_polling(bot, allowed_updates=["message"])
```

---

## ✅ That’s it!
