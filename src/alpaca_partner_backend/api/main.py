"""alpaca-partner-backend REST API."""

import json
import logging
import traceback

import coloredlogs
from alpaca.common.exceptions import APIError as BrokerAPIError
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pymongo.errors import DuplicateKeyError

from alpaca_partner_backend.api.routes import accounts, assets, users

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.0:8000",
        "localhost:8000",
        "localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(assets.router)
app.include_router(users.router)


@app.exception_handler(BrokerAPIError)
def handle_broker_api_errors(request: Request, exc: BrokerAPIError) -> JSONResponse:
    """BrokerAPIError converter."""
    traceback.print_tb(exc.__traceback__)
    return JSONResponse(
        status_code=exc.status_code,
        content=json.loads(exc.response.content).get("message", None),
    )


@app.exception_handler(DuplicateKeyError)
def handle_mongo_duplicate_errors(
    request: Request,
    exc: DuplicateKeyError,
) -> JSONResponse:
    """Key error converter."""
    traceback.print_tb(exc.__traceback__)
    exc_dict: dict[str, str] = exc.details.get("keyValue", {}) if exc.details else {}
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=f"Another {list(exc_dict.keys())[0]} already exists in the database with the value {list(exc_dict.values())[0]}"
        if exc_dict
        else exc.details,
    )


@app.exception_handler(KeyError)
def handle_key_errors(
    request: Request,
    exc: KeyError,
) -> JSONResponse:
    """Key error converter."""
    traceback.print_tb(exc.__traceback__)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=f"There was a key error on the {exc.args[0]} field.",
    )


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Reset testing overrides before running the server
    app.dependency_overrides = {}
    # Remove all handlers associated with the root logger object.
    # for handler in logging.root.handlers:
    # logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()


@app.get("/")
def docs() -> RedirectResponse:
    """Automatically redirect homepage to docs."""
    return RedirectResponse(url="/docs")
