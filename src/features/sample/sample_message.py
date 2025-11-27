from fastapi import status

SAMPLE_NOT_FOUND_ERROR = "sample_not_found"
SAMPLE_EMPTY_UPDATE_ERROR = "sample_empty_update"

SAMPLE_ERROR_STATUS = {
    SAMPLE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
    SAMPLE_EMPTY_UPDATE_ERROR: status.HTTP_400_BAD_REQUEST,
}

