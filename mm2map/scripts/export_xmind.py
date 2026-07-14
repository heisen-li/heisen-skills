import sys
import os
import json
import zipfile
import uuid
import time
from xml.etree.ElementTree import Element, SubElement, tostring

sys.stdout.reconfigure(encoding='utf-8')


def _gen_id():
    return uuid.uuid4().hex


def _add_children(parent_elem, children):
    if not children:
        return

    children_elem = SubElement(parent_elem, "children")
    topics_elem = SubElement(children_elem, "topics")
    topics_elem.set("type", "attached")

    for child in children:
        topic_elem = SubElement(topics_elem, "topic")
        topic_elem.set("id", _gen_id())
        topic_elem.set("timestamp", str(int(time.time() * 1000)))

        title_elem = SubElement(topic_elem, "title")
        title_elem.text = child.get("title", "")

        if "notes" in child and child["notes"]:
            notes_elem = SubElement(topic_elem, "notes")
            notes_plain = SubElement(notes_elem, "plain")
            notes_plain.text = child["notes"]

        if "children" in child and child["children"]:
            _add_children(topic_elem, child["children"])


def generate_xmind(mindmap_data, output_path):
    root_title = mindmap_data.get("title", mindmap_data.get("root", "Root Topic"))
    children = mindmap_data.get("children", [])
    sheet_title = mindmap_data.get("sheet_title", "Sheet 1")

    ts = str(int(time.time() * 1000))

    content_root = Element("xmap-content")
    content_root.set("xmlns", "urn:xmind:xmap:xmlns:content:2.0")
    content_root.set("xmlns:fo", "urn:xmind:xmap:xmlns:format:2.0")
    content_root.set("xmlns:svg", "urn:xmind:xmap:xmlns:svg:2.0")
    content_root.set("xmlns:xhtml", "urn:xmind:xmap:xmlns:xhtml:2.0")
    content_root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    content_root.set("timestamp", ts)
    content_root.set("version", "2.0")

    sheet = SubElement(content_root, "sheet")
    sheet.set("id", _gen_id())
    sheet.set("timestamp", ts)

    root_topic = SubElement(sheet, "topic")
    root_topic.set("id", _gen_id())
    root_topic.set("timestamp", ts)

    root_title_elem = SubElement(root_topic, "title")
    root_title_elem.text = root_title

    _add_children(root_topic, children)

    sheet_title_elem = SubElement(sheet, "title")
    sheet_title_elem.text = sheet_title

    content_xml = tostring(content_root, encoding="unicode", xml_declaration=True)

    metadata_root = Element("metadata")
    metadata_root.set("xmlns", "urn:xmind:xmap:xmlns:metadata:2.0")
    metadata_root.set("timestamp", ts)
    author_elem = SubElement(metadata_root, "Author")
    author_elem.text = "mm2map"

    metadata_xml = tostring(metadata_root, encoding="unicode", xml_declaration=True)

    manifest_root = Element("manifest")
    manifest_root.set("xmlns", "urn:xmind:xmap:xmlns:manifest:1.0")

    fe_content = SubElement(manifest_root, "file-entry")
    fe_content.set("full-path", "content.xml")
    fe_content.set("media-type", "text/xml")

    fe_meta_inf = SubElement(manifest_root, "file-entry")
    fe_meta_inf.set("full-path", "META-INF/")
    fe_meta_inf.set("media-type", "")

    fe_manifest = SubElement(manifest_root, "file-entry")
    fe_manifest.set("full-path", "META-INF/manifest.xml")
    fe_manifest.set("media-type", "text/xml")

    fe_metadata = SubElement(manifest_root, "file-entry")
    fe_metadata.set("full-path", "metadata.xml")
    fe_metadata.set("media-type", "text/xml")

    manifest_xml = tostring(manifest_root, encoding="unicode", xml_declaration=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.xml", content_xml)
        zf.writestr("metadata.xml", metadata_xml)
        zf.writestr("META-INF/manifest.xml", manifest_xml)


def parse_mermaid_to_tree(mermaid_text):
    lines = mermaid_text.strip().split('\n')
    root_title = ""
    children = []
    stack = []

    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            continue

        indent = 0
        temp = stripped
        while temp.startswith('  ') or temp.startswith('\t'):
            if temp.startswith('  '):
                indent += 1
                temp = temp[2:]
            else:
                indent += 1
                temp = temp[1:]

        text = temp.strip()

        if text.startswith('mindmap'):
            continue

        if 'root((' in text and '))' in text:
            start = text.index('root((') + 6
            end = text.index('))')
            root_title = text[start:end]
            node = {"title": root_title, "children": []}
            stack = [(0, node)]
            continue

        node = {"title": text, "children": []}

        while stack and stack[-1][0] >= indent:
            stack.pop()

        if stack:
            stack[-1][1]["children"].append(node)

        stack.append((indent, node))

    if stack:
        return stack[0][1]
    return {"title": root_title or "Root", "children": children}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Arguments required",
            "message": "Usage: python export_xmind.py <mermaid_text_or_file> <output_xmind_path>",
            "example": "python export_xmind.py mindmap_video.mmd mindmap_video.xmind"
        }, ensure_ascii=False))
        sys.exit(1)

    source = sys.argv[1]
    output_path = sys.argv[2]

    if os.path.exists(source):
        with open(source, 'r', encoding='utf-8') as f:
            mermaid_text = f.read()
    else:
        mermaid_text = source

    tree = parse_mermaid_to_tree(mermaid_text)

    source_name = os.path.splitext(os.path.basename(output_path))[0]
    tree["sheet_title"] = source_name

    try:
        generate_xmind(tree, output_path)
        print(json.dumps({
            "status": "success",
            "output_file": output_path,
            "format": "XMind (.xmind)",
            "message": f"XMind file generated: {output_path}. Can be opened directly in XMind application."
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": "Failed to generate XMind file",
            "message": str(e)
        }, ensure_ascii=False))
        sys.exit(1)
