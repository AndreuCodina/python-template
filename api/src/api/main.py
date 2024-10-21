from fastapi import FastAPI

from domain.domain_printer import DomainPrinter

app = FastAPI()


@app.get("/")
async def root() -> str:
    DomainPrinter().print()
    return "Hello"
