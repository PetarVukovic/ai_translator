from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from logger import MyLogger

log = MyLogger(name="AI-Subtitle", log_file="logs/app.log")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def save_to_disk(file: UploadFile):
    try:
        with open("srt_files/" + file.filename, "wb") as f:
            f.write(await file.read())
        log.info("Succes saved to disk")
    except Exception as e:
        log.error(f"Error {e} occured while saving to disk")


async def open_srt_file(file_path: str):

    with open("srt_files/manna4.srt", "r", encoding="utf-8") as f:
        srt_text = f.read()
        print(srt_text[:500].strip())


async def translate_chunck(srt_chunck: str, language: str = "english"):
    try:
        pass
    except Exception as e:
        log.error(f"An error occcured in translate_chunck,error:{e}")


@app.post("/uploadSrt")
async def upload_srt(file: UploadFile = File(...)):
    log.info("Starting with uploaded srt file")
    await save_to_disk(file)
