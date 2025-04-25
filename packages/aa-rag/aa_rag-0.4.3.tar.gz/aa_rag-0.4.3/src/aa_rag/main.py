from fastapi import FastAPI
from fastmcp import FastMCP

from aa_rag import setting
from aa_rag.exceptions import (
    handle_exception_error,
    handel_file_not_found_error,
)
from aa_rag.router import qa, solution, index, retrieve, statistic, delete

app = FastAPI()
app.include_router(qa.router)
app.include_router(solution.router)
app.include_router(index.router)
app.include_router(retrieve.router)
app.include_router(statistic.router)
app.include_router(delete.router)
app.add_exception_handler(Exception, handle_exception_error)
app.add_exception_handler(FileNotFoundError, handel_file_not_found_error)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/default")
async def default():
    return setting.model_dump()


def startup():
    import uvicorn

    uvicorn.run(app, host=setting.server.host, port=setting.server.port)

if __name__ == "__main__":
    mcp = FastMCP.from_fastapi(app, name="AARAG")

    mcp.run()
    startup()
