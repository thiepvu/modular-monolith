# File Management Module Setup Guide

## Overview

Complete file management module with:
- ✅ File upload/download
- ✅ Access control (public/private/shared)
- ✅ File metadata management
- ✅ Size and type validation
- ✅ Download tracking
- ✅ Clean Architecture structure

## Installation Steps

### 1. Copy Module Files

Copy all files from the 3 artifacts to:
```
src/modules/file_management/
├── domain/               # Artifact 1
├── application/          # Artifact 2
├── infrastructure/       # Artifact 2
└── presentation/         # Artifact 3
```

### 2. Install Additional Dependencies

Add to `requirements.txt`:
```
aiofiles==23.2.1
python-multipart==0.0.6
```

Install:
```bash
pip install aiofiles python-multipart
```

### 3. Add Model Import to Migrations

Edit `src/infrastructure/migrations/env.py`:

```python
# Add this import
from src.modules.file_management.infrastructure.persistence.models import FileModel
```

### 4. Create Migration

```bash
python scripts/migrate.py --create "Add file management tables"
```

### 5. Run Migration

```bash
python scripts/migrate.py --upgrade
```

### 6. Create Upload Directory

```bash
mkdir -p uploads
```

### 7. Start Server

```bash
python src/main.py
```

## API Endpoints

Visit: http://localhost:8000/api/docs

### Upload File
```http
POST /api/v1/files/upload
Content-Type: multipart/form-data

file: [binary]
description: "My document"
is_public: false
```

### Get File Metadata
```http
GET /api/v1/files/{file_id}
```

### Download File
```http
GET /api/v1/files/{file_id}/download
```

### List Files
```http
GET /api/v1/files?page=1&page_size=20&owner_only=true
```

### Update File
```http
PUT /api/v1/files/{file_id}
Content-Type: application/json

{
  "description": "Updated description",
  "is_public": true
}
```

### Share File
```http
POST /api/v1/files/{file_id}/share
Content-Type: application/json

{
  "user_id": "uuid-here"
}
```

### Delete File
```http
DELETE /api/v1/files/{file_id}
```

## Features

### File Upload
- Validates file size (max 100MB)
- Validates MIME types
- Generates unique filenames
- Stores files in user-specific directories

### Access Control
- **Private**: Only owner can access
- **Public**: Everyone can access
- **Shared**: Specific users can access

### File Types Supported
- Images: JPEG, PNG, GIF, WebP
- Documents: PDF, Word, Excel
- Text: Plain text, CSV
- Archives: ZIP, RAR

### Business Logic
- Download tracking
- File size limits
- MIME type validation
- Path traversal prevention
- Ownership verification

## Configuration

### Change Upload Directory

Edit `FileStorageService` initialization:
```python
storage_service = FileStorageService(storage_path="your/custom/path")
```

### Change File Size Limit

Edit `File` entity:
```python
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
```

### Add Allowed File Types

Edit `File` entity:
```python
ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'video/mp4',  # Add video
    'audio/mpeg',  # Add audio
    # ... more types
]
```

## Testing

### Unit Test Example

```python
def test_create_file():
    file = File.create(
        name="test.pdf",
        original_name="document.pdf",
        path="uploads/test.pdf",
        size=1024,
        mime_type="application/pdf",
        owner_id=UUID("...")
    )
    
    assert file.name == "test.pdf"
    assert file.size.bytes == 1024
```

### API Test Example

```python
@pytest.mark.asyncio
async def test_upload_file(client):
    files = {"file": ("test.txt", b"test content", "text/plain")}
    
    response = await client.post(
        "/api/v1/files/upload",
        files=files
    )
    
    assert response.status_code == 201
```

## Integration with User Module

To integrate with authentication:

1. Replace `MOCK_USER_ID` in routes
2. Add authentication dependency:

```python
from src.modules.auth.dependencies import get_current_user

@router.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user)
):
    # Use current_user.id instead of MOCK_USER_ID
    pass
```

## Security Considerations

✅ **Path Traversal Protection**: Validates paths
✅ **File Type Validation**: Only allowed MIME types
✅ **Size Limits**: Prevents huge uploads
✅ **Access Control**: Owner/public/shared permissions
✅ **Unique Filenames**: Prevents overwrites

## Troubleshooting

### Upload Fails
- Check `uploads/` directory exists
- Verify file size under limit
- Check MIME type is allowed

### Download Fails
- Verify user has access
- Check file exists in storage
- Verify path is correct

### Migration Error
- Ensure FileModel imported in env.py
- Check PostgreSQL is running
- Verify database URL in .env

## Next Steps

1. Add authentication integration
2. Add file preview generation
3. Add virus scanning
4. Add cloud storage (S3, Azure)
5. Add file versioning
6. Add thumbnail generation for images
7. Add search functionality
8. Add file categories/tags

## Success! 🎉

Your file management module is ready!

Test it at: http://localhost:8000/api/docs