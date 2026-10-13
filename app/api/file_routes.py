from fastapi import APIRouter

from app.models.schemas import (
    CsvSearchRequest
)

from app.services.csv_file_service import (
    csv_file_service
)


router = APIRouter(
    prefix="/api/files",
    tags=["Files"]
)


@router.post("/scan")
def scan_files():

    files = csv_file_service.scan_files()

    return {
        "count": len(files),
        "files": files
    }


@router.get("")
def get_files():

    files = csv_file_service.get_files()

    return {
        "count": len(files),
        "files": files
    }


@router.post("/search")
def search_files(
    request: CsvSearchRequest
):

    results = csv_file_service.search_files(
        request.stock_symbol,
        request.question or ""
    )

    return {
        "count": len(results),
        "files": results
    }