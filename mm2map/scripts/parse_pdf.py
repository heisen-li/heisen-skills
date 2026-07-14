import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

def parse_pdf(pdf_path):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print(json.dumps({
                "error": "pymupdf (PyMuPDF) not installed",
                "message": "Run: pip install pymupdf, then reinstall via install_deps.ps1 -Install"
            }, ensure_ascii=False))
            sys.exit(1)

    if not os.path.exists(pdf_path):
        print(json.dumps({
            "error": "File not found",
            "message": f"PDF file not found: {pdf_path}"
        }, ensure_ascii=False))
        sys.exit(1)

    if not pdf_path.lower().endswith('.pdf'):
        print(json.dumps({
            "error": "Unsupported format",
            "message": "Only .pdf files are supported."
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(json.dumps({
            "error": "Failed to open PDF",
            "message": str(e)
        }, ensure_ascii=False))
        sys.exit(1)

    pages_data = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if not text.strip():
            continue

        paragraphs = []
        raw_lines = text.split('\n')
        current_para = ""
        for line in raw_lines:
            stripped = line.strip()
            if not stripped:
                if current_para.strip():
                    paragraphs.append(current_para.strip())
                    current_para = ""
                continue

            is_heading = False
            font_sizes = []
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for line_obj in block["lines"]:
                        for span in line_obj["spans"]:
                            if stripped in span["text"]:
                                font_sizes.append(span["size"])

            if font_sizes:
                avg_size = sum(font_sizes) / len(font_sizes)
                all_sizes = []
                for p in range(len(doc)):
                    pb = doc[p].get_text("dict")["blocks"]
                    for b in pb:
                        if b["type"] == 0:
                            for l in b["lines"]:
                                for s in l["spans"]:
                                    all_sizes.append(s["size"])
                if all_sizes:
                    median_size = sorted(all_sizes)[len(all_sizes) // 2]
                    if avg_size > median_size * 1.3:
                        is_heading = True

            level = 0 if is_heading else 1
            current_para += (stripped + " ")

        if current_para.strip():
            paragraphs.append(current_para.strip())

        content_items = []
        for para in paragraphs:
            is_heading = False
            font_sizes_check = []
            blocks_check = page.get_text("dict")["blocks"]
            for block in blocks_check:
                if block["type"] == 0:
                    for line_obj in block["lines"]:
                        for span in line_obj["spans"]:
                            if para[:50] in span["text"]:
                                font_sizes_check.append(span["size"])
            if font_sizes_check:
                all_sizes_page = []
                for b in blocks_check:
                    if b["type"] == 0:
                        for l in b["lines"]:
                            for s in l["spans"]:
                                all_sizes_page.append(s["size"])
                if all_sizes_page:
                    median_s = sorted(all_sizes_page)[len(all_sizes_page) // 2]
                    if sum(font_sizes_check) / len(font_sizes_check) > median_s * 1.3:
                        is_heading = True

            content_items.append({
                "text": para,
                "level": 0 if is_heading else 1
            })

        title = ""
        if content_items:
            headings = [c for c in content_items if c["level"] == 0]
            if headings:
                title = headings[0]["text"]
            else:
                title = content_items[0]["text"][:80]

        pages_data.append({
            "page_number": page_num + 1,
            "title": title,
            "content": content_items,
            "raw_text": text.strip()
        })

    doc.close()

    result = {
        "source": pdf_path,
        "total_pages": len(doc),
        "pages_with_text": len(pages_data),
        "pages": pages_data
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No PDF file path provided",
            "message": "Usage: python parse_pdf.py <pdf_file_path>"
        }, ensure_ascii=False))
        sys.exit(1)

    parse_pdf(sys.argv[1])
