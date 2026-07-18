from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=SecretStr(
        "")
)
