# Read current file
with open('routes/cover_letter.py', 'r') as f:
    lines = f.readlines()

# Find the download function and fix Form defaults
new_lines = []
for i, line in enumerate(lines):
    if 'version_index: int = Form(0)' in line:
        line = line.replace('Form(0)', 'Form(default=0)')
    if 'format: str = Form("pdf")' in line:
        line = line.replace('Form("pdf")', 'Form(default="pdf")')
    new_lines.append(line)

# Write back
with open('routes/cover_letter.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Fixed Form parameter defaults")
