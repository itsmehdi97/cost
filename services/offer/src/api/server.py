from fastapi import FastAPI
from fastapi.responses import Response

from api.routes import router  as api_router
from core import tasks





def get_application():
    app = FastAPI(title='offer')

    app.include_router(api_router, prefix="/api")


    app.add_event_handler("startup", tasks.create_start_app_handler(app))

    
    return app


app = get_application()

@app.get("/ping")
async def ping():
    return Response(status_code=204)