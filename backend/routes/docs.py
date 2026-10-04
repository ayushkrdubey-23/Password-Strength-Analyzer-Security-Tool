"""OpenAPI specification and Swagger UI routes."""

from flask import Blueprint, jsonify, make_response


docs_bp = Blueprint("docs", __name__)


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Password Strength Analyzer API",
        "version": "1.0.0",
        "description": (
            "API documentation for the Password Strength Analyzer "
            "and Security Suggestion Tool. Use synthetic passwords "
            "for testing. Never submit real account passwords."
        ),
    },
    "servers": [
        {
            "url": "/",
            "description": "Current Flask application",
        }
    ],
    "tags": [
        {"name": "Health", "description": "Application health"},
        {"name": "Password Analysis", "description": "Analyze password strength"},
        {"name": "Password Generator", "description": "Generate secure passwords"},
        {"name": "Password Policy", "description": "Check password policy compliance"},
    ],
    "paths": {
        "/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Check application health",
                "responses": {
                    "200": {
                        "description": "Application is running",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "message": "Application is running successfully.",
                                    "application": "Password Strength Analyzer",
                                    "environment": "development",
                                }
                            }
                        },
                    }
                },
            }
        },
        "/api/analyze": {
            "post": {
                "tags": ["Password Analysis"],
                "summary": "Analyze password strength",
                "description": (
                    "Analyzes a synthetic password. The submitted password "
                    "is not returned or stored by this endpoint. "
                    "Rate limit: 10 requests per minute per client."
                ),
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["password"],
                                "properties": {
                                    "password": {
                                        "type": "string",
                                        "description": "Synthetic password for demonstration.",
                                        "example": "Violet!Cedar#74Moon",
                                    }
                                },
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Password analysis completed",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": {
                                        "score": 95,
                                        "category": "VERY STRONG",
                                        "findings": [],
                                        "suggestions": [],
                                    },
                                }
                            }
                        },
                    },
                    "400": {"description": "Invalid request body"},
                    "415": {"description": "JSON content type required"},
                    "429": {"description": "Rate limit exceeded"},
                    "500": {"description": "Analysis could not be completed"},
                },
            }
        },
        "/api/generate": {
            "post": {
                "tags": ["Password Generator"],
                "summary": "Generate a secure password",
                "description": (
                    "Generates a password using Python's secrets module. "
                    "The generated password is returned in the response. "
                    "Rate limit: 10 requests per minute per client."
                ),
                "requestBody": {
                    "required": False,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "length": {
                                        "type": "integer",
                                        "minimum": 8,
                                        "maximum": 128,
                                        "default": 20,
                                        "example": 20,
                                    },
                                    "include_lowercase": {
                                        "type": "boolean",
                                        "default": True,
                                    },
                                    "include_uppercase": {
                                        "type": "boolean",
                                        "default": True,
                                    },
                                    "include_digits": {
                                        "type": "boolean",
                                        "default": True,
                                    },
                                    "include_symbols": {
                                        "type": "boolean",
                                        "default": True,
                                    },
                                },
                            },
                            "example": {
                                "length": 20,
                                "include_lowercase": True,
                                "include_uppercase": True,
                                "include_digits": True,
                                "include_symbols": True,
                            },
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Password generated successfully",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": {
                                        "password": "SyntheticGenerated!82",
                                        "length": 21,
                                        "message": "Secure password generated successfully.",
                                    },
                                }
                            }
                        },
                    },
                    "400": {"description": "Invalid generation options"},
                    "415": {"description": "JSON content type required"},
                    "429": {"description": "Rate limit exceeded"},
                },
            }
        },
        "/api/policy/check": {
            "post": {
                "tags": ["Password Policy"],
                "summary": "Check password policy compliance",
                "description": (
                    "Checks a synthetic password against ten default "
                    "policy requirements. The submitted password is "
                    "not returned or stored. "
                    "Rate limit: 10 requests per minute per client."
                ),
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["password"],
                                "properties": {
                                    "password": {
                                        "type": "string",
                                        "description": "Synthetic password for demonstration.",
                                        "example": "Violet!Cedar#74Moon",
                                    }
                                },
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Policy check completed",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": {
                                        "policy_name": "Default Password Security Policy",
                                        "compliant": True,
                                        "total_checks": 10,
                                        "passed_checks": 10,
                                        "failed_checks": 0,
                                        "checks": [],
                                        "recommendations": [],
                                        "privacy": {
                                            "password_returned": False,
                                            "password_stored": False,
                                            "password_logged": False,
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "400": {"description": "Invalid request body"},
                    "415": {"description": "JSON content type required"},
                    "429": {"description": "Rate limit exceeded"},
                    "500": {"description": "Internal error"},
                },
            }
        },
    },
}


@docs_bp.route("/openapi.json", methods=["GET"])
def openapi_json():
    """Return the OpenAPI specification."""

    response = make_response(jsonify(OPENAPI_SPEC))
    response.headers["Cache-Control"] = "no-store"
    return response


@docs_bp.route("/apidocs", methods=["GET"])
def swagger_ui():
    """Serve the Swagger UI page."""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>Password Strength Analyzer API Docs</title>
    <link
        rel="stylesheet"
        href="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui.css"
    >
    <style>
        body {
            margin: 0;
            background: #f5f7fb;
        }

        .topbar {
            display: none;
        }

        .swagger-ui .info {
            margin: 28px 0;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function () {
            window.ui = SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui",
                deepLinking: true,
                displayRequestDuration: true,
                persistAuthorization: false,
                validatorUrl: null,
                supportedSubmitMethods: ["get", "post"],
                presets: [
                    SwaggerUIBundle.presets.apis
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>"""

    response = make_response(html)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["Cache-Control"] = "no-store"

    return response
