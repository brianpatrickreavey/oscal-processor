from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.router import router as api_router
from src.api.inventory import router as inventory_router
from src.api.system_characteristics import router as system_char_router
from src.api.responsible_roles import router as roles_router
from src.api.control_implementation import router as control_impl_router
from src.api.assessment_result import router as assessment_result_router
from src.api.links_references import router as links_references_router
from src.api.attachment import router as attachment_router


app = FastAPI()

app.include_router(api_router, prefix="/api")
app.include_router(system_char_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(control_impl_router, prefix="/api")
app.include_router(assessment_result_router, prefix="/api")
app.include_router(links_references_router, prefix="/api")
app.include_router(attachment_router, prefix="/api")
app.include_router(inventory_router, prefix="/api/inventory")
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.responses import FileResponse

@app.get("/")
def serve_index():
    return FileResponse("static/index_claude.html")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")
