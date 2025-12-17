from fastapi import APIRouter, HTTPException
from typing import List
import logging
from app.models.request import IngestRequest
from app.models.response import IngestResponse, ErrorResponse
from app.services.ingest_service import IngestService

logger = logging.getLogger(__name__)
router = APIRouter()
ingest_service = IngestService()

@router.post("/ingest",
             response_model=IngestResponse,
             responses={
                 200: {"description": "Content ingested successfully"},
                 400: {"model": ErrorResponse, "description": "Invalid request"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def ingest_endpoint(ingest_request: IngestRequest):
    try:
        if not ingest_request.content or not ingest_request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        if not ingest_request.source or not ingest_request.source.strip():
            raise HTTPException(status_code=400, detail="Source cannot be empty")

        result = await ingest_service.ingest_content(
            content=ingest_request.content,
            source=ingest_request.source,
            metadata=ingest_request.metadata,
            chapter=ingest_request.chapter,
            section=ingest_request.section
        )
        return IngestResponse(
            success=result["success"],
            document_id=result["document_id"],
            message=result["message"],
            embedding_created=result["embedding_created"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/ingest/batch")
async def batch_ingest_endpoint(ingest_requests: List[IngestRequest]):
    try:
        contents = []
        for req in ingest_requests:
            if not req.content.strip() or not req.source.strip():
                raise HTTPException(status_code=400, detail="Content or source cannot be empty")
            contents.append({
                'content': req.content,
                'source': req.source,
                'metadata': req.metadata,
                'chapter': req.chapter,
                'section': req.section
            })
        results = await ingest_service.batch_ingest(contents)
        return {"results": results, "total_processed": len(results)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch ingest endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/ingest/health")
async def ingest_health():
    try:
        test_result = await ingest_service.check_content_exists("test", "test_source")
        return {"status": "healthy", "service": "ingest"}
    except Exception as e:
        logger.error(f"Ingest health check failed: {e}")
        raise HTTPException(status_code=500, detail="Ingest service not healthy")
