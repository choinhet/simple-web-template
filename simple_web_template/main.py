import logging

import uvicorn
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from simple_web_template.repositories.message_repository import MessageRepository
from simple_web_template.services.messaging_service import MessagingService

from simple_web_template.model.data_structures import SendDTO, Conversation

app = FastAPI()
log = logging.getLogger("simple_web_template")

message_repository = MessageRepository()
messaging_service = MessagingService(message_repository)

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


@app.post("/send/", response_class=JSONResponse)
async def send(send_dto: SendDTO):
    conversation = messaging_service.find_conversation(send_dto.conversation_id)

    if conversation is None:
        return JSONResponse(
            status_code=404, content={"message": "Conversation not found"}
        )

    conversation.messages.append(send_dto.message)
    return JSONResponse(status_code=200, content=conversation.model_dump_json())


@app.get("/conversation", response_class=JSONResponse)
async def get_conversation(_: Request, id: uuid.UUID):
    conversation = messaging_service.find_conversation(id)

    if conversation is None:
        return JSONResponse(
            status_code=404, content={"message": "Conversation not found"}
        )

    return JSONResponse(status_code=200, content=conversation.model_dump_json())

@app.get("/conversations", response_class=JSONResponse)
async def list_conversations(_: Request):
    conversations = messaging_service.list_conversations()
    return JSONResponse(status_code=200, content=[c.model_dump_json() for c in conversations])

@app.post("/start", response_class=JSONResponse)
async def start(sender: str, receiver: str):
    conversation = Conversation(users=[sender, receiver])
    messaging_service.add_conversation(conversation)
    return JSONResponse(status_code=201, content=conversation.model_dump_json())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="localhost", port=8000)
