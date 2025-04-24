from typing import Optional, List

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""

    page_content: str

    vector: Optional[list[float]] = None

    metadata: Optional[dict] = Field(default_factory=dict)

    kb_id: Optional[List[str]] = None

    kb: Optional[List[str]] = None

    label: Optional[List[str]] = None

    id: Optional[str] = None

    content_split: Optional[str] = None

    create_time: Optional[str] = None

    title: Optional[str] = None

    slots: Optional[List[str]] = None

    question: Optional[List[str]] = None

    institution: Optional[List[str]] = None

    authors: Optional[List[str]] = None

    abstract: Optional[str] = None

    file_id: Optional[str] = None

    chunk_index: Optional[int] = None
