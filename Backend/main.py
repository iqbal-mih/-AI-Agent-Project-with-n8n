from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import httpx
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS configuration - adjust origins as needed for your clients
# You can set ALLOW_ALL_ORIGINS=1 in the environment for development to allow any origin.
allow_all = os.environ.get("ALLOW_ALL_ORIGINS", "0") == "1"

if allow_all:
    allow_origins = ["*"]
else:
    # common local dev origins - add your frontend origin (port) here if needed
    allow_origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if allow_all:
    logger = logging.getLogger(__name__)
    logger.warning("CORS: allow_all is enabled (ALLOW_ALL_ORIGINS=1). This is insecure for production.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Simple request-logging middleware for debugging OPTIONS/CORS preflight
@app.middleware("http")
async def log_requests(request, call_next):
    try:
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        # log key headers relevant to CORS
        origin = request.headers.get("origin")
        acr_method = request.headers.get("access-control-request-method")
        acr_headers = request.headers.get("access-control-request-headers")
        if origin or acr_method or acr_headers:
            logger.info(f"CORS headers - Origin: {origin}, ACR-Method: {acr_method}, ACR-Headers: {acr_headers}")
    except Exception:
        logger.exception("Failed to log request headers")
    return await call_next(request)


# Handle preflight OPTIONS explicitly for /chat to ensure proper CORS response headers
@app.options("/chat")
async def chat_options(request: Request):
    origin = request.headers.get("origin")

    # Determine allowed origin value for the response
    if allow_all:
        allowed_origin = "*"
    else:
        # If request origin is in our allowlist, mirror it back; otherwise, don't allow
        allowed_origin = origin if origin in allow_origins else None

    headers = {}
    if allowed_origin:
        headers["Access-Control-Allow-Origin"] = allowed_origin
        headers["Access-Control-Allow-Methods"] = ", ".join(["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"])
        headers["Access-Control-Allow-Headers"] = request.headers.get("access-control-request-headers", "*")
        # Only include allow-credentials when not using wildcard origin
        if allow_all is False:
            headers["Access-Control-Allow-Credentials"] = "true"

    # Return 200 with CORS headers (if any). If origin not allowed, return 403.
    if allowed_origin:
        return Response(status_code=200, headers=headers)
    else:
        return Response(status_code=403, content="Origin not allowed")

class ChatRequest(BaseModel):
    user_query: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Forward chat request to n8n webhook
    """
    webhook_url = "https://iqbalmih.app.n8n.cloud/webhook/ai-agent"
    
    payload = {
        "user_query": request.user_query,
        "session_id": request.session_id
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=payload, timeout=180.0)
            # Log status and body for debugging
            logger.info(f"Webhook response: {response.status_code}")
            logger.debug(f"Webhook response body: {response.text}")

            # If the webhook returned JSON, forward it as JSON with the same status code.
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type.lower():
                try:
                    return JSONResponse(content=response.json(), status_code=response.status_code)
                except Exception:
                    # Fallback to raw text if JSON parsing fails
                    return Response(content=response.text, status_code=response.status_code, media_type=content_type)

            # For non-JSON responses, forward raw content and content-type
            return Response(content=response.content, status_code=response.status_code, media_type=content_type or "text/plain")
    except httpx.HTTPStatusError as e:
        # HTTP error with response (4xx/5xx) - forward the upstream response if available
        resp = e.response
        body = resp.text if resp is not None else str(e)
        logger.error(f"Webhook HTTPStatusError: {str(e)}")
        if resp is not None:
            # Try to mirror the upstream response (status code + body + content-type)
            content_type = resp.headers.get("content-type", "text/plain")
            try:
                return Response(content=resp.content, status_code=resp.status_code, media_type=content_type)
            except Exception:
                logger.exception("Failed to forward upstream error response; falling back to 502")
        raise HTTPException(status_code=502, detail=f"Webhook HTTP error: {body}")
    except httpx.HTTPError as e:
        # Network-level errors (connection, timeout, etc.)
        logger.error(f"Error calling webhook: {repr(e)}")
        # If the exception has a response attribute, try to include it for debugging
        resp = getattr(e, "response", None)
        if resp is not None:
            try:
                return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "text/plain"))
            except Exception:
                logger.exception("Failed to forward response attached to HTTPError")
        raise HTTPException(status_code=502, detail=f"Webhook error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "FastAPI Chat Server Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
