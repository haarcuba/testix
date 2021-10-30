import dataclasses

@dataclasses.dataclass
class CallCharacter:
    awaitable: bool = False
    is_sync_context: bool = False
    is_async_context: bool = False

    @property
    def is_context(self) -> bool:
        return self.is_sync_context or self.is_async_context

    @property
    def normal(self):
        remarkable = self.awaitable or self.is_context
        return not remarkable
