"""
convert_report_to_pdf.py
------------------------
Converts rsrapport_Universitetet_i_Agder_UIA_Project_Controlling_Earned_Value_EV_Analysis.md
into a stunning, executive PDF using Playwright (Chromium headless) with Edward Tufte styling.
"""

import sys
import os
import re

MD_PATH = r"C:\Users\frank\Desktop\UIA\rsrapport_Universitetet_i_Agder_UIA_Project_Controlling_Earned_Value_EV_Analysis.md"
PDF_PATH = r"C:\Users\frank\Desktop\UIA\rsrapport_Universitetet_i_Agder_UIA_Project_Controlling_Earned_Value_EV_Analysis.pdf"
TEMP_HTML = r"C:\Users\frank\Desktop\UIA\rsrapport_temp_print.html"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

# Convert markdown to clean HTML
import markdown
html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="no">
<head>
  <meta charset="UTF-8">
  <title>Årsrapport Universitetet i Agder (UIA) - Project Controlling & Earned Value (EV) Analysis</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 16mm 14mm 16mm 14mm;
      @bottom-right {{
        content: "Side " counter(page);
        font-size: 8pt;
        color: #64748b;
        font-family: 'Inter', sans-serif;
      }}
    }}
    
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      font-size: 9.5pt;
      line-height: 1.5;
      color: #0f172a;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }}
    
    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 18pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #0284c7;
      padding-bottom: 6px;
      margin-top: 0;
      margin-bottom: 8px;
    }}
    
    h2 {{
      font-family: 'Outfit', sans-serif;
      font-size: 13pt;
      font-weight: 600;
      color: #0369a1;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 14pt;
      margin-bottom: 6pt;
      page-break-after: avoid;
    }}
    
    h3 {{
      font-family: 'Outfit', sans-serif;
      font-size: 11pt;
      font-weight: 600;
      color: #1e293b;
      margin-top: 10pt;
      margin-bottom: 4pt;
      page-break-after: avoid;
    }}
    
    p {{
      margin: 0 0 6pt 0;
      text-align: justify;
    }}
    
    strong {{
      font-weight: 600;
      color: #0f172a;
    }}
    
    /* Edward Tufte Table Styling */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8.5pt;
      margin: 8pt 0 12pt 0;
      page-break-inside: avoid;
    }}
    
    th {{
      border-top: 1.5pt solid #0f172a;
      border-bottom: 1pt solid #0f172a;
      padding: 4pt 6pt;
      text-align: left;
      font-weight: 600;
      color: #0f172a;
      text-transform: uppercase;
      font-size: 7.5pt;
      letter-spacing: 0.3px;
    }}
    
    th:nth-child(2), th:nth-child(3), th:nth-child(4),
    th:nth-child(5), th:nth-child(6), th:nth-child(7),
    th:nth-child(8), th:nth-child(9), th:nth-child(10),
    th:nth-child(11), th:nth-child(12), th:nth-child(13),
    th:nth-child(14), th:nth-child(15) {{
      text-align: right;
    }}
    
    td {{
      border-bottom: 0.5pt solid #e2e8f0;
      padding: 3.5pt 6pt;
      vertical-align: top;
    }}
    
    td:nth-child(2), td:nth-child(3), td:nth-child(4),
    td:nth-child(5), td:nth-child(6), td:nth-child(7),
    td:nth-child(8), td:nth-child(9), td:nth-child(10),
    td:nth-child(11), td:nth-child(12), td:nth-child(13),
    td:nth-child(14), td:nth-child(15) {{
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
    }}
    
    tr:last-child td {{
      border-bottom: 1.5pt solid #0f172a;
      font-weight: 600;
    }}
    
    code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0369a1;
    }}
    
    ul, ol {{
      margin: 0 0 8pt 0;
      padding-left: 18pt;
    }}
    
    li {{
      margin-bottom: 3pt;
    }}
    
    hr {{
      border: 0;
      border-top: 1px solid #cbd5e1;
      margin: 12pt 0;
    }}
    
    .header-box {{
      background: #f8fafc;
      border-left: 3.5pt solid #0284c7;
      padding: 8pt 12pt;
      margin-bottom: 12pt;
      font-size: 8.5pt;
      color: #334155;
    }}
  </style>
</head>
<body>
  {html_body}
</body>
</html>
"""

with open(TEMP_HTML, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated HTML for print.")

# Use Playwright to render PDF
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{TEMP_HTML.replace('\\\\', '/')}")
    page.pdf(
        path=PDF_PATH,
        format="A4",
        print_background=True,
        margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"}
    )
    browser.close()

if os.path.exists(TEMP_HTML):
    os.remove(TEMP_HTML)

print(f"Successfully generated executive PDF at: {PDF_PATH}")
