from pydantic import BaseModel, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    age: int = Field(ge=1, le=120)
    course: str = Field(min_length=1, max_length=120)


class StudentUpdate(StudentCreate):
    pass


class StudentOut(StudentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    document_id: int | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    document_id: int | None = None
    note: str
