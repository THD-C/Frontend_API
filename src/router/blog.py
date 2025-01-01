from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request, Query
from grpc import RpcError
from pydantic import BaseModel

from src.connections import blog_stub
from user import user_type_pb2
from blog import blog_pb2
from src.utils.auth import verify_user

from src.utils.logger import logger

blog_router = APIRouter(tags=["Blog"])


class BlogRequest(BaseModel):
    language: str
    title: str
    content: str


class BlogUpdateRequest(BaseModel):
    language: str
    title: str
    content: str
    path: str


@blog_router.post("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Creation of blog failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "Details of blog",
        "content": {
            "application/json": {
                "example": {
                    "title": "test title",
                    "language": "en",
                    "path": "test-title",
                    "content": "This is test content."
                }
            }
        }
    }
}, description='Creates new blog')
def add_blog(request: Request,
             blog_request: BlogRequest):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if jwt_payload["user_type"] < user_type_pb2.USER_TYPE_BLOGGER_USER:
        logger.warning("Unauthorized user tried to add blog")
        raise HTTPException(401, detail="unauthorized_user_for_method")

    blog_request_message: blog_pb2.BlogContent = blog_pb2.BlogContent(language=blog_request.language,
                                                                      title=blog_request.title,
                                                                      content=blog_request.content)

    try:
        blog_response: blog_pb2.BlogContent = blog_stub.AddBlog(blog_request_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if blog_response.path == "*":
        logger.error("Blog has not been added!")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(blog_response,
                             preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)


@blog_router.put("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Update of blog failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "Details of updated blog",
        "content": {
            "application/json": {
                "example": {
                    "title": "test title",
                    "language": "en",
                    "path": "test-title",
                    "content": "This is test content."
                }
            }
        }
    }
}, description='Updates already existing blog. Uses path and language as reference.')
def update_blog(request: Request,
                blog_update_request: BlogUpdateRequest):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if jwt_payload["user_type"] < user_type_pb2.USER_TYPE_BLOGGER_USER:
        logger.warning("Unauthorized user tried to add blog")
        raise HTTPException(401, detail="unauthorized_user_for_method")

    blog_request_message: blog_pb2.BlogContent = blog_pb2.BlogContent(**blog_update_request.model_dump())

    try:
        blog_response: blog_pb2.BlogContent = blog_stub.UpdateBlog(blog_request_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if blog_response.path == "*":
        logger.error("Blog has not been updated!")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(blog_response,
                             preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)


@blog_router.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "No blogs found"
    },
    200: {
        "description": "Details of blog",
        "content": {
            "application/json": {
                "example": {
                    "Blogs": [
                        {
                            "title": "string",
                            "language": "string",
                            "path": "string",
                            "content": "string"
                        },
                        {
                            "title": "string",
                            "language": "string",
                            "path": "string-1",
                            "content": "string"
                        }
                    ]
                }
            }
        }
    }
}, description='Lists all blogs matching to applied filters')
def get_blog(request: Request,
             title: str | None = Query("", description="Blog title to filter by", ),
             language: str | None = Query("", description="Blog language to filter by"),
             path: str | None = Query("", description="Blog path to filter by")):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    blog_filter_message: blog_pb2.FilterBlogMessage = blog_pb2.FilterBlogMessage(title=title,
                                                                                 language=language,
                                                                                 path=path)

    try:
        blog_response: blog_pb2.BlogList = blog_stub.GetBlogs(blog_filter_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(blog_response.Blogs) == 0:
        logger.info("No blogs found")
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(blog_response,
                             preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)


@blog_router.delete("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Deletion of blog failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "Details of deleted blog",
        "content": {
            "application/json": {
                "example": {
                    "title": "test title",
                    "language": "en",
                    "path": "test-title",
                    "content": "This is test content."
                }
            }
        }
    }
}, description='Deletes blog record specified with path and language')
def delete_blog(request: Request,
                path: str = Query(..., description="Path to blog"),
                language: str = Query(..., description="Blog language"), ):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if jwt_payload["user_type"] < user_type_pb2.USER_TYPE_BLOGGER_USER:
        logger.warning("Unauthorized user tried to add blog")
        raise HTTPException(401, detail="unauthorized_user_for_method")

    blog_delete_message: blog_pb2.FilterBlogMessage = blog_pb2.FilterBlogMessage(path=path,
                                                                                 language=language)

    try:
        blog_delete_response: blog_pb2.BlogContent = blog_stub.DeleteBlog(blog_delete_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if blog_delete_response.path == "*":
        logger.error("Blog has not been deleted")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(blog_delete_response,
                             preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)
