import base64
import binascii
import logging
import pyfiglet as pf
from typing import List

from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    # UnauthenticatedUser,
    AuthCredentials
)

from strawberry.asgi import GraphQL
from strawberry.subscriptions import GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL

from felicity.api.api_v1.api import api_router  # noqa
from felicity.apps.core.channel import broadcast
from felicity.core.config import settings  # noqa
from felicity.core.repeater import repeat_every
from felicity.gql.schema import gql_schema  # noqa
from felicity.gql.deps import get_current_active_user
from felicity.apps.job.sched import felicity_halt_workforce
from felicity.apps.job.sched import felicity_workforce_init
from felicity.init import initialize_felicity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FelicityAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() == 'basic':
                decoded = base64.b64decode(credentials).decode("ascii")
                username, _, password = decoded.partition(":")
                # TODO: You'd want to verify the username and password here if needed
            elif scheme.lower() == 'bearer':
                """"get is active user from token"""
                user = await get_current_active_user(credentials)
                username, _, password = user.auth.user_name, None, None
            else:
                raise AuthenticationError(f'UnKnown Authentication Backend: {scheme.lower()}')

            return AuthCredentials(["authenticated"]), SimpleUser(username)

        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError(f'Invalid auth credentials: {exc}')


flims = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@flims.on_event("startup")
async def startup():
    # print("\n")
    # print(pf.Figlet("doom").renderText("FELICITY  LIMS"))  # "puffy"
    await initialize_felicity()
    felicity_workforce_init()


@flims.on_event("startup")
@repeat_every(seconds=3)  # 60 * 60 = 1 hour
async def always_and_forever():
    # print(datetime.now())
    pass


@flims.on_event("shutdown")
async def shutdown():
    felicity_halt_workforce()


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    flims.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

flims.add_middleware(
    AuthenticationMiddleware,
    backend=FelicityAuthBackend()
)

graphql_app = GraphQL(gql_schema, subscription_protocols=[GRAPHQL_WS_PROTOCOL, GRAPHQL_TRANSPORT_WS_PROTOCOL])

flims.include_router(api_router, prefix=settings.API_V1_STR)
flims.add_route("/felicity-gql", graphql_app)
flims.add_websocket_route("/subscriptions", graphql_app, "felicity-subscriptions")


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@flims.websocket("/ws/{after_uid}")
async def websocket_endpoint(websocket: WebSocket, after_uid: int):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client {after_uid}: {data}")


from starlette.concurrency import run_until_first_complete


async def chatroom_ws(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket}),
    )


async def chatroom_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="activities", message=message)


async def chatroom_ws_sender(websocket):
    async with broadcast.subscribe(channel="activities") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


flims.add_websocket_route("/chatter", chatroom_ws, "chatroom_ws")
import json


async def get_streams(websocket):
    async with broadcast.subscribe(channel="activities") as subscriber:
        async for event in subscriber:
            data = json.loads(json.dumps(event.message.marshal_simple(), indent=4, sort_keys=True, default=str))
            await websocket.send_json(data)


async def stream_socket(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (get_streams, {"websocket": websocket}),
    )


flims.add_websocket_route("/streamer", stream_socket, "stream-only")
