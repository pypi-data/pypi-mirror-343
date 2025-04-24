# app/api/routes/router.py
import logging
from fastapi import APIRouter, Request
from pydantic import BaseModel
from ollama import AsyncClient
import asyncio

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


async def get_response_from_ollama(host, model_name, query_request, source_name):
    logger = logging.getLogger(__name__)
    ollama_client = AsyncClient(host=host)

    try:
        message = {"role": "user", "content": query_request.query}
        response = await ollama_client.chat(
            model=model_name, messages=[message], stream=False
        )

        content = (
            response.message.content
            if hasattr(response, "message") and hasattr(response.message, "content")
            else str(response)
        )

        logger.debug(f"Extracted content from {host}: {content}")
        return {"response": content, "source": source_name}
    except Exception as e:
        logger.error(f"Error processing request for {host}: {e}")
        return {"error": str(e), "source": source_name}


@router.post("/query")
async def run_query(query_request: QueryRequest, request: Request):
    logger = logging.getLogger(__name__)
    logger.debug(f"Received request: {query_request}")

    tasks = [
        get_response_from_ollama(
            "http://192.168.109.227:11434",
            "granite3.3:latest",
            query_request,
            "server1",
        ),
        get_response_from_ollama(
            "http://192.168.109.218:11434",
            "aya-expanse:latest",
            query_request,
            "server2",
        ),
    ]

    responses = await asyncio.gather(*tasks)

    formatted_responses = []
    for response in responses:
        if "error" in response:
            formatted_responses.append(
                {
                    "response": f"<strong>Error:</strong> {response['error']}",
                    "source": response["source"],
                }
            )
        else:
            formatted_responses.append(
                {"response": response["response"], "source": response["source"]}
            )

    if len(formatted_responses) == 2:
        summary_query = f""" Task: Generate a concise, accurate summary by cross-referencing the following responses.
        Correct any discrepancies, remove hallucinations, and ensure factual integrity.

        Original Query:
        {query_request.query}

        Source Responses: 1. Response A:
        {formatted_responses[0]['response']} 2. Response B:
        {formatted_responses[1]['response']}

        Requirements:
        - Prioritize factual consistency between sources.
        - Resolve conflicting information.
        - Eliminate redundant or fabricated content.
        - Ensure the summary reflects only validated information.
        - Remove hallucinations.
        - Don't note incorrect information, just omit it.
        - Don't mention information was removed or discrepancies, just omit it.
        - Write "Summary:\n" then write the summary.
        """

        summary_task = get_response_from_ollama(
            "http://192.168.109.217:11434",
            "qwq:32b",
            QueryRequest(query=summary_query),
            "Summary Server",
        )

        summary_response = await summary_task

        if "error" in summary_response:
            formatted_responses.append(
                {
                    "response": f"<strong>Error:</strong> {summary_response['error']}",
                    "source": summary_response["source"],
                }
            )
        else:
            formatted_responses.append(
                {
                    "response": summary_response["response"],
                    "source": summary_response["source"],
                }
            )

    logger.debug(f"Formatted responses: {formatted_responses}")

    return {"responses": formatted_responses}
