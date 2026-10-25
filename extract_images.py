import os
import zipfile
import shutil

docx_user = r"C:\Users\Jazlynn Barrios\.gemini\antigravity\brain\00a87bd4-13fd-43a3-b507-a149210ed287\.user_uploaded\media_1792244635611_881eaa72.docx"
extract_dir = r"c:\proyecto_final\proyecto_final\extracted_media"

os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(docx_user, 'r') as z:
    for name in z.namelist():
        if name.startswith('word/media/'):
            filename = os.path.basename(name)
            if filename:
                with open(os.path.join(extract_dir, filename), 'wb') as f:
                    f.write(z.read(name))

print("Extracted images:", len(os.listdir(extract_dir)))
