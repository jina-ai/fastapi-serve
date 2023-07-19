from fastapi import FastAPI, HTTPException, Query, UploadFile

from fastapi_serve import JinaBlobStorage

app = FastAPI()


def get_chain(path: str):
    from langchain import OpenAI
    from langchain.chains import RetrievalQA
    from langchain.document_loaders import PyPDFLoader
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import FAISS

    index = FAISS.from_documents(
        documents=PyPDFLoader(path).load_and_split(),
        embedding=OpenAIEmbeddings(),
    )
    return RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=index.as_retriever(),
    )


async def index_pdf(uri: str):
    file_path = "./temp_file"
    await JinaBlobStorage.download(uri, file_path)
    return get_chain(file_path)


@app.post("/upload")
async def upload_file(file: UploadFile, public: bool = False):
    try:
        print(f'Uploading file {file.filename} to Jina Blob Storage')
        uri = await JinaBlobStorage.upload(file, file.filename, public=public)
        return {"uri": uri}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/answer")
async def answer_question(uri: str = Query(...), question: str = Query(...)) -> str:
    try:
        print(f'Answering question {question} from {uri}')
        chain = await index_pdf(uri)
        return chain(question).get('result', 'No answer found')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
