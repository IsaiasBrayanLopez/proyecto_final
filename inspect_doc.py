import zipfile
import xml.etree.ElementTree as ET

docx_user = r"C:\Users\Jazlynn Barrios\.gemini\antigravity\brain\00a87bd4-13fd-43a3-b507-a149210ed287\.user_uploaded\media_1792244635611_881eaa72.docx"

with zipfile.ZipFile(docx_user, 'r') as z:
    xml_content = z.read('word/document.xml')
    rels_content = z.read('word/_rels/document.xml.rels')

# Parse relationships to map rId to image filename
rels_root = ET.fromstring(rels_content)
rel_map = {}
for child in rels_root:
    rId = child.attrib.get('Id')
    target = child.attrib.get('Target')
    if target and 'media/' in target:
        rel_map[rId] = target.split('/')[-1]

# Parse document structure
doc_root = ET.fromstring(xml_content)
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

items = []
for p in doc_root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
    full_text = "".join(texts).strip()
    
    # Check for blip r:embed
    imgs = []
    for blip in p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
        embed = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if embed and embed in rel_map:
            imgs.append(rel_map[embed])
            
    if full_text or imgs:
        items.append({'text': full_text, 'imgs': imgs})

print(f"Total paragraphs/items with text or images: {len(items)}")
for i, item in enumerate(items[:35]):
    print(f"[{i}] Text: {item['text'][:60]} | Imgs: {item['imgs']}")
