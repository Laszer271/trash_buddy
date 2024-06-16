import re
from time import time

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from vision import GptVision
from assistant_rag import RAG

import logging
logger = logging.getLogger(__name__)

#---------------INIT APP------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#---------------TYPES------------------
class ChatMessage(BaseModel):
    base64: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

def _process_answer(answer):
    answer = re.sub('\[\d+\]', '', answer)

    instructions = re.split(r'\d+\.', answer)
    instructions = [s.strip() for s in instructions if s.strip() != '']
    instructions = [f'{i+1}. ' + s for i, s in enumerate(instructions)]
    return instructions

@app.post("/chat", response_model=dict)
async def getMessage(message:ChatMessage):
    logger.info("Otrzymałem wiadomość ", len(message.base64))
    assert message.base64 is not None, "Message must be provided"

    start_time = time()
    vision = GptVision()
    response = vision.describe_image(message.base64)
    print(response)
    logger.info(response)
    print(f"Processing time: {time() - start_time}")

    # rag = RAG()
    # answer = rag.find_similar_category(response.content)
    # print(answer)
    # logger.info(answer)

    # # answear = "Test"
    # answer_processed = _process_answer(answer.value)
    # print(answer_processed)
    # print(type(answer_processed))
    # return {"message": answer_processed}
    return {"message": _process_answer(response.content)}