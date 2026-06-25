"""Split documents into retrieval-sized chunks."""

from __future__ import annotations

import logging

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE

logger = logging.getLogger(__name__)

HEADERS_TO_SPLIT = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
]


def split_documents(documents: list[Document]) -> list[Document]:
    if not documents:
        return []

    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT)
    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Document] = []

    for doc in documents:
        header_sections = header_splitter.split_text(doc.page_content)

        for section in header_sections:
            section.metadata = {**doc.metadata, **section.metadata}

            if len(section.page_content) <= CHUNK_SIZE:
                chunks.append(section)
                continue

            sub_chunks = size_splitter.split_documents([section])
            chunks.extend(sub_chunks)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index
        section_title = (
            chunk.metadata.get("header_3")
            or chunk.metadata.get("header_2")
            or chunk.metadata.get("header_1")
            or ""
        )
        if section_title:
            chunk.metadata["section_title"] = section_title

    logger.info("Split %d documents into %d chunks", len(documents), len(chunks))
    return chunks
