import os
import uuid
import logging
import base64
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import List, Union

from api.services.interfaces.IUplaodFileService import IUplaodFileService  # Fixed typo in interface name

logger = logging.getLogger(__name__)


class UploadFileService(IUplaodFileService):

    def __init__(self):
        """Initialize the service with a base upload directory."""
        self.base_upload_dir = os.path.join(settings.BASE_DIR, 'upload')

    def _ensure_upload_folder_exists(self, subfolder: str) -> str:
        """Ensure the upload folder exists; create it if necessary."""
        upload_folder = os.path.join(self.base_upload_dir, subfolder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            logger.info(f"Created upload folder: {upload_folder}")
        return upload_folder

    def _validate_file_extension(self, file_name: str, allowed_extensions: List[str]) -> bool:
        """Validate the file extension against a list of allowed extensions."""
        ext = file_name.split('.')[-1].lower()
        return ext in allowed_extensions

    def _validate_file_size(self, file_size: int, max_size_mb: int) -> bool:
        """Validate the file size against a maximum size limit in MB."""
        return file_size <= max_size_mb * 1024 * 1024

    def delete_image_file(self, file_name_with_path: str, folder_name: str) -> bool:
        """Delete a file from the specified folder."""
        upload_folder = os.path.join(self.base_upload_dir, folder_name)
        path = os.path.join(upload_folder, file_name_with_path)
        
        if not os.path.exists(path):
            logger.warning(f"Image file not found: {path}")
            return False
        
        os.remove(path)
        logger.info(f"Image file {path} deleted successfully.")
        return True

    def upload_file_to_gallery(self, images: List[InMemoryUploadedFile], subfolder: str) -> List[str]:
        """Upload multiple image files to the specified subfolder."""
        upload_folder = self._ensure_upload_folder_exists(subfolder)
        uploaded_files = []

        for image in images:
            if not isinstance(image, InMemoryUploadedFile):
                uploaded_files.append("InvalidFile")
                continue

            # Validate file extension
            if not self._validate_file_extension(image.name, ['jpg', 'png', 'jpeg']):
                uploaded_files.append("NotImage")
                continue

            # Validate file size (3MB limit)
            if not self._validate_file_size(image.size, 3):
                uploaded_files.append("OverSizeLimit")
                continue

            # Generate unique file name
            ext = image.name.split('.')[-1].lower()
            unique_file_name = f"{uuid.uuid4()}.{ext}"
            file_path = os.path.join(upload_folder, unique_file_name)

            # Save the file in chunks
            try:
                with open(file_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                uploaded_files.append(unique_file_name)
                logger.info(f"File uploaded successfully: {unique_file_name}")
            except Exception as e:
                logger.error(f"Error uploading file {image.name}: {e}")
                uploaded_files.append("UploadFailed")

        return uploaded_files

    def upload_pdf_file(self, file: InMemoryUploadedFile, subfolder: str) -> str:
        """Upload a single PDF file to the specified subfolder."""
        upload_folder = self._ensure_upload_folder_exists(subfolder)

        # Validate file extension
        if not self._validate_file_extension(file.name, ['pdf']):
            return "NotPdf"

        # Generate unique file name
        unique_file_name = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(upload_folder, unique_file_name)

        # Save the file in chunks
        try:
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            logger.info(f"PDF file uploaded successfully: {unique_file_name}")
            return unique_file_name
        except Exception as e:
            logger.error(f"Error uploading PDF file {file.name}: {e}")
            return "UploadFailed"

    def upload_file_as_base64(self, base64_string: str, file_name: str, subfolder: str) -> str:
        """Upload a base64-encoded file to the specified subfolder."""
        upload_folder = self._ensure_upload_folder_exists(subfolder)

        # Validate file extension
        if not self._validate_file_extension(file_name, ['jpg', 'png', 'jpeg']):
            return "NotImage"

        # Generate unique file name
        ext = file_name.split('.')[-1].lower()
        unique_file_name = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(upload_folder, unique_file_name)

        # Decode and save the base64 file
        try:
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(base64_string))
            logger.info(f"Base64 file uploaded successfully: {unique_file_name}")
            return unique_file_name
        except Exception as e:
            logger.error(f"Error uploading base64 file: {e}")
            return "UploadFailed"