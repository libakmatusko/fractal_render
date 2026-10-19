"""OpenAPI HTTP interface for the image processor."""

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import UnidentifiedImageError

from modules.processor import SUPPORTED_EXTENSIONS, process_image


app = FastAPI(title="Fractal Render API", version="0.1.0")


@app.post("/process", summary="Process an image")
async def process_uploaded_image(file: UploadFile) -> Response:
    """Process an uploaded image and return the result as a downloadable file."""
    extension = ""
    if file.filename:
        extension = file.filename.rsplit(".", maxsplit=1)[-1].lower()
        if "." in file.filename:
            extension = f".{extension}"

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported image file type")

    image_data = await file.read()
    try:
        processed_image = process_image(image_data)
    except (UnidentifiedImageError, OSError) as error:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image") from error

    return Response(
        content=processed_image,
        media_type=file.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="processed{extension}"'},
    )
