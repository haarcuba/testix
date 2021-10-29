import dataclasses

@dataclasses.dataclass
class Modifiers:
    awaitable: bool = False
    is_context: bool = False
    is_async_context: bool = False
