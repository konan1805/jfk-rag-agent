import os

import psycopg
from agents import function_tool
from dotenv import load_dotenv
from openai import OpenAI
from pgvector import Vector
from pgvector.psycopg import register_vector


def search_documents(
    query: str,
    client: OpenAI,
    conn,
    limit: int = 5,
):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query,
    )

    query_embedding = response.data[0].embedding

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                document_id,
                filename,
                url,
                chunk_index,
                content,
                1 - (embedding <=> %s) AS similarity
            FROM jfk_documents
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (
                Vector(query_embedding),
                Vector(query_embedding),
                limit,
            ),
        )

        return cur.fetchall()


@function_tool
def search_jfk_documents(query: str) -> str:
    """Search the JFK document database for information relevant to a question.

    Args:
        query: The information to search for in the JFK documents.
    """
    print(f"\n[TOOL CALLED] search_jfk_documents")
    print(f"[QUERY] {query}\n")
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    client = OpenAI()

    with psycopg.connect(database_url) as conn:
        register_vector(conn)

        results = search_documents(
            query=query,
            client=client,
            conn=conn,
            limit=5,
        )

    formatted_results = []

    for result in results:
        (
            document_id,
            filename,
            url,
            chunk_index,
            content,
            similarity,
        ) = result

        formatted_results.append(
            f"""
Filename: {filename}
URL: {url}
Chunk: {chunk_index}
Similarity: {similarity:.4f}
Content:
{content}
"""
        )

    return "\n---\n".join(formatted_results)