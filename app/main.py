from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from sqladmin import Admin
import app
from app.admin import CompanyAdmin, FieldAdmin, DksAdmin, spchAdmin
from app.api.v1.router import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import engine

app = FastAPI()

app.include_router(router)

ORIGINS = [
    "http://10.7.114.224:4001"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
admin = Admin(app, engine)
admin.add_view(CompanyAdmin)
admin.add_view(FieldAdmin)
admin.add_view(DksAdmin)
admin.add_view(spchAdmin)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)