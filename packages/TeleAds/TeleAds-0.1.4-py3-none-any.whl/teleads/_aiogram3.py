from aiogram import BaseMiddleware

class BapAIOgram3Middleware(BaseMiddleware):
    def __init__(self, api_key: str) -> None:
        self._bap = Bap(api_key)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        needUpdate = await self._bap.handle_update(event.to_python())

        if needUpdate:
            return await handler(event, data)