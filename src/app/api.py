import os
from http import HTTPStatus
import json

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
import jsonpatch

from apischema.encoder import encode_to_json_response, encode_error_to_json_response
from apischema.validator import validate_todo_entry
from entities import TodoEntry
from persistence.repository import TodoEntryRepository
from persistence.mapper import init_mapper

from usecases import (
    get_todo_entry,
    create_todo_entry,
    update_existing_todo_entry,
    UseCaseError,
    NotFoundError,
)

mapper = init_mapper()
repository = TodoEntryRepository(mapper)


async def get_todo(request: Request) -> Response:
    """
    summary: Finds TodoEntry by id
    parameters:
        - name: id
          in: path
          description: TodoEntry id
          required: true
          schema:
            type: integer
            format: int64
    responses:
        "200":
            description: Object was found.
            examples:
                {
                    "id": 1,
                    "summary": "Lorem Ipsum",
                    "detail": null,
                    "created_at": "2022-09-27T17:29:06.183775+00:00",
                    "tags": []
                }
        "404":
            description: Object was not found
    """
    try:
        identifier = request.path_params["id"]  # TODO: add validation

        entity = await get_todo_entry(identifier=identifier, repository=repository)
        content = encode_to_json_response(entity=entity)

    except NotFoundError:
        return Response(
            content=None,
            status_code=HTTPStatus.NOT_FOUND,
            media_type="application/json",
        )

    return Response(content=content, media_type="application/json")


async def create_new_todo_entry(request: Request) -> Response:
    """
    summary: Creates new TodoEntry
    responses:
        "201":
            description: TodoEntry was created.
            examples:
                {
                    "id": 1,
                    "summary": "Lorem Ipsum",
                    "detail": null,
                    "created_at": "2022-09-27T17:29:06.183775+00:00",
                    "tags": []
                }
        "422":
            description: Validation error.
        "500":
            description: Something went wrong, try again later.
    """
    data = await request.json()
    errors = validate_todo_entry(raw_data=data)
    if errors:
        return Response(
            content=encode_error_to_json_response(error=errors),
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            media_type="application/json",
        )

    try:
        entity = TodoEntry(**data)
        entity = await create_todo_entry(entity=entity, repository=repository)
        content = encode_to_json_response(entity=entity)
    except UseCaseError:
        return Response(
            content=None,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )

    return Response(
        content=content, status_code=HTTPStatus.CREATED, media_type="application/json"
    )


async def update_todo_entry(request: Request) -> Response:
    """
    summary: Tags TodoEntry
    parameters:
        - name: id
          in: path
          description: TodoEntry id
          required: true
          schema:
            type: integer
            format: int64
    responses:
        "204":
            description: TodoEntry was updated with tags.
            examples:
                {
                    "summary": "Lorem Ipsum",
                    "detail": null,
                    "created_at": "2022-09-05T18:07:19.280040+00:00",
                    "tags": ["important"]
                }
        "422":
            description: Validation error.
        "500":
            description: Something went wrong, try again later.
    """
    try:
        identifier = request.path_params["id"]

        entity = await get_todo_entry(identifier=identifier, repository=repository)
        entity = json.loads(encode_to_json_response(entity=entity))

    except NotFoundError:
        return Response(
            content=None,
            status_code=HTTPStatus.NOT_FOUND,
            media_type="application/json",
        )

    patch = await request.json()
    data = jsonpatch.apply_patch(entity, patch)
    errors = validate_todo_entry(raw_data=data)
    if errors:
        return Response(
            content=encode_error_to_json_response(error=errors),
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            media_type="application/json",
        )

    try:
        updated_entity = TodoEntry(**data)
        updated_entity = await update_existing_todo_entry(
            identifier=identifier, updated_entity=updated_entity, repository=repository
        )
        content = encode_to_json_response(entity=updated_entity)
    except UseCaseError:
        return Response(
            content=None,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )

    return Response(content=content, media_type="application/json")


app = Starlette(
    debug=True,
    routes=[
        Route("/todo/", create_new_todo_entry, methods=["POST"]),
        Route("/todo/{id:int}/", get_todo, methods=["GET"]),
        Route("/todo/{id:int}/", update_todo_entry, methods=["PATCH"]),
    ],
)
