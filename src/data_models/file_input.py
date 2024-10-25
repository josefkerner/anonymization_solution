from pydantic import BaseModel

class Input(BaseModel):
    type: str  # can be:  word, pdf, linkedin or web
    payload: str  # byte array encoded into base 64 string in ascii format
    # example how to send input to backend: base64.encode(text).decode('ascii')