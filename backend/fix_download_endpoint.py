# Fix download endpoint to accept request body
with open('routes/cover_letter.py', 'r') as f:
    content = f.read()

# Replace the download function
old_func = '''@router.post("/download")
async def download_cover_letter(
    cover_letter_id: str = Form(...),
    version_index: int = Form(default=0),
    format: str = Form(default="pdf"),
    user: dict = Depends(get_current_user)
):
    """Download cover letter as PDF or DOCX"""
    cover_letter = await db.cover_letters.find_one(
        {"id": cover_letter_id, "user_id": user["id"]},
        {"_id": 0}
    )'''

new_func = '''class CoverLetterDownloadRequest(BaseModel):
    cover_letter_id: str
    version_index: int = 0
    format: str = "pdf"


@router.post("/download")
async def download_cover_letter(
    request: CoverLetterDownloadRequest,
    user: dict = Depends(get_current_user)
):
    """Download cover letter as PDF or DOCX"""
    cover_letter = await db.cover_letters.find_one(
        {"id": request.cover_letter_id, "user_id": user["id"]},
        {"_id": 0}
    )'''

content = content.replace(old_func, new_func)

# Also need to update references to the old parameters
content = content.replace('if version_index >= len(versions):', 'if request.version_index >= len(versions):')
content = content.replace('version = versions[version_index]', 'version = versions[request.version_index]')
content = content.replace('if format == "docx":', 'if request.format == "docx":')

with open('routes/cover_letter.py', 'w') as f:
    f.write(content)

print("✅ Fixed download endpoint to accept JSON body")
