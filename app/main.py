from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.logger import MyLogger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import httpx

log = MyLogger(name="AI-Subtitle", log_file="logs/app.log")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
languages = [
    # "English",
    # "Spanish",
    "French",
    # "Portuguese",
    # "Urdu",
    # "German",
    # "Turkish",
]

n8n_webhook_url = "https://ivanakristova7.app.n8n.cloud/webhook-test/cd76f64a-1eb8-4e66-995c-cb8c33e4e31a"


async def translate(chunkcs: str, language: str = "English") -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0)
    sys = SystemMessage(
        "You are my translator of christianity srt files.You only returning transalted srt file with \n indicating new line.,dont include anythine lse only pure timestrempts with transaltion return"
    )
    human = HumanMessage(
        content=f"Please transalte this in {language} here is srt file chunck: {chunkcs} "
    )
    results = await llm.ainvoke([sys, human])
    return results.content


import os


async def transalte_chuncks(srt_as_array: list[str]):
    num_chunks = 10
    total = len(srt_as_array)
    step = max(1, total // num_chunks)

    # 📁 Kreiraj direktorij ako ne postoji
    output_dir = "translations"
    os.makedirs(output_dir, exist_ok=True)

    async with httpx.AsyncClient() as client:
        for lang in languages:
            translated_srt = []
            for i in range(0, len(srt_as_array), step):
                chuncks = srt_as_array[i : i + step]
                chunks_to_translate = "\n".join(chuncks)
                translated_chunk = await translate(chunks_to_translate, lang)
                translated_srt.append(translated_chunk)

            translated_srt_as_str = (
                "\n".join(translated_srt).encode("utf-8").decode("unicode_escape")
            )

            # 💾 Zapis na disk
            file_path = os.path.join(output_dir, f"{lang.lower()}_translated.srt.txt")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(translated_srt_as_str)
                log.info(f"Saved translation to disk: {file_path}")
            except Exception as e:
                log.error(f"Error writing file {file_path}: {e}")

            # 🔁 Slanje na n8n webhook
            response = await client.post(
                n8n_webhook_url,
                json={
                    "language": lang,
                    "translated_srt": translated_srt_as_str,
                },
            )

            # Log / yield
            yield {"lang": lang, "status": response.status_code}


async def srt_2_list(srt_file: bytes):
    try:
        srt_file_str = srt_file.decode("utf-8")
        srt_file_list = srt_file_str.strip().split("\n\n")
        return srt_file_list
    except Exception as e:
        log.error(f"Error {e} occured while converting srt to list")


@app.post("/uploadSrt")
async def upload_srt(file: UploadFile = File(...)):
    log.info("Starting with uploaded srt file")
    srt_file = await file.read()
    srt_file_list = await srt_2_list(srt_file)
    async for result in transalte_chuncks(srt_file_list):
        log.info(f"Sent translation for {result['lang']}, status: {result['status']}")

    return {"message": "Translation started and sending to n8n."}
