import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import item, file, directory
from api.utils import camelize_query_parameters_with_no_custom_alias
from api.middlewares.files_system_exception_handler import FilesSystemExceptionHandlerMiddleware

load_dotenv()

app = FastAPI()
allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',')


app.add_middleware(FilesSystemExceptionHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(item.router)
app.include_router(file.router)
app.include_router(directory.router)

camelize_query_parameters_with_no_custom_alias(app)
