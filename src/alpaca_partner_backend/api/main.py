"""alpaca-partner-backend REST API."""

import logging

import coloredlogs
from alpaca_partner_backend.api.routes import accounts, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Reset testing overrides before running the server
    app.dependency_overrides = {}
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()


@app.get("/")
def docs() -> RedirectResponse:
    """Automatically redirect homepage to docs."""
    return RedirectResponse(url="/docs")
