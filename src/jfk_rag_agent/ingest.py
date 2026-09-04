import os

import psycopg
from datasets import load_dataset
from dotenv import load_dotenv
from openai import OpenAI
from pgvector import Vector
from pgvector.psycopg import register_vector


def chunk_text(
    text: str,
    chunk_size: int = 1500,
    overlap: int = 200,
) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def is_valid_content(content: str) -> bool:
    if not content:
        return False

    cleaned = content.strip()

    if len(cleaned) < 200:
        return False

    return True


def main() -> None:
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    dataset = load_dataset("aurelio-ai/jfk-files")

    valid_documents = []

    for document in dataset["train"]:
        content = document["content"]

        if not is_valid_content(content):
            continue

        chunks = chunk_text(content)

        valid_documents.append(
            {
                "id": document["id"],
                "filename": document["filename"],
                "url": document["url"],
                "date": document["date"],
                "chunks": chunks,
            }
        )

    chunk_records = []

    for document in valid_documents:
        for chunk_index, chunk in enumerate(document["chunks"]):
            chunk_records.append(
                {
                    "document_id": document["id"],
                    "filename": document["filename"],
                    "url": document["url"],
                    "date": document["date"],
                    "chunk_index": chunk_index,
                    "content": chunk,
                }
            )

    client = OpenAI()
    batch_size = 100

    with psycopg.connect(database_url) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            for start in range(0, len(chunk_records), batch_size):
                batch = chunk_records[start:start + batch_size]

                texts = [
                    item["content"]
                    for item in batch
                ]

                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=texts,
                )

                for item, embedding_data in zip(
                    batch,
                    response.data,
                ):
                    cur.execute(
                        """
                        INSERT INTO jfk_documents (
                            document_id,
                            filename,
                            url,
                            document_date,
                            chunk_index,
                            content,
                            embedding
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            item["document_id"],
                            item["filename"],
                            item["url"],
                            item["date"],
                            item["chunk_index"],
                            item["content"],
                            Vector(
                                embedding_data.embedding
                            ),
                        ),
                    )

                conn.commit()

                print(
                    f"Inserted "
                    f"{min(start + batch_size, len(chunk_records))} "
                    f"of {len(chunk_records)} chunks"
                )


if __name__ == "__main__":
    main()