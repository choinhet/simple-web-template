from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="simple_web_template/static"), name="static")
templates = Jinja2Templates(directory="simple_web_template/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = dict(
        request=request,
        description="This is a simple web template",
        title="Simple Web Template",
    )
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
