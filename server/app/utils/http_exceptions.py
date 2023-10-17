from flask import json


def http_exception_handler(e):
    response = e.get_response()

    response.data = json.dumps({
        "error": f"{e.name} - {e.description}",
        # "message": "the requested operation did not get completed"
    })

    response.content_type = "application/json"
    return response
