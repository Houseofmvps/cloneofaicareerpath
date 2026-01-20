#!/usr/bin/env python3
import re

# Read the file
with open('routes/cover_letter.py', 'r') as f:
    content = f.read()

# Find and replace the download function signature
old_pattern = r'@router\.post\("/download"\)\nasync def download_cover_letter\(\s*cover_letter_id: str = Form\(\.\.\.\),\s*version_index: int = Form\(0\),\s*format: str = Form\("pdf"\),\s*user: dict = Depends\(get_current_user\)\s*\):'

new_code = '''@router.post("/download")
async def download_cover_letter(
    cover_letter_id: str = Form(...),
    version_index: int = Form(default=0),
    format: str = Form(default="pdf"),
    user: dict = Depends(get_current_user)
):'''

content = re.sub(old_pattern, new_code, content, flags=re.MULTILINE)

# Write back
with open('routes/cover_letter.py', 'w') as f:
    f.write(content)

print("✅ Fixed download endpoint parameters")
