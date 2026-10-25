import zipfile
import xml.etree.ElementTree as ET

docx_user = r"C:\Users\Jazlynn Barrios\.gemini\antigravity\brain\00a87bd4-13fd-43a3-b507-a149210ed287\.user_uploaded\media_1792244635611_881eaa72.docx"

with zipfile.ZipFile(docx_user, 'r') as z:
    xml_content = z.read('word/document.xml')
    rels_content = z.read('word/_rels/document.xml.rels')

rels_root = ET.fromstring(rels_content)
rel_map = {}
for child in rels_root:
    rId = child.attrib.get('Id')
    target = child.attrib.get('Target')
    if target and 'media/' in target:
        rel_map[rId] = target.split('/')[-1]

doc_root = ET.fromstring(xml_content)

items = []
for p in doc_root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
    full_text = "".join(texts).strip()
    
    imgs = []
    for blip in p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
        embed = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if embed and embed in rel_map:
            imgs.append(rel_map[embed])
            
    if full_text or imgs:
        items.append({'text': full_text, 'imgs': imgs})

with open("doc_structure.txt", "w", encoding="utf-8") as out:
    for i, item in enumerate(items):
        out.write(f"[{i}] Text: {item['text']} | Imgs: {item['imgs']}\n")

print("Saved to doc_structure.txt")
