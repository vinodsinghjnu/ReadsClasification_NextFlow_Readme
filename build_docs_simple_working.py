import markdown
import os

# Read the markdown file
with open("README.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Define modern Apple/GitHub style CSS
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    body { 
        font-family: 'Inter', -apple-system, sans-serif; 
        display: flex; 
        margin: 0; 
        color: #24292f; 
        background: #ffffff;
    }
    
    /* Left side Table of Contents */
    .toc-container { 
        width: 320px; 
        position: fixed; 
        height: 100vh; 
        overflow-y: auto; 
        padding: 30px; 
        box-sizing: border-box;
        border-right: 1px solid #d0d7de; 
        background: #f6f8fa; 
    }
    
    .toc-container h3 {
        margin-top: 0;
        font-size: 16px;
        color: #57606a;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .toc-container ul { 
        list-style: none; 
        padding-left: 15px; 
    }
    
    .toc-container > div > ul {
        padding-left: 0;
    }
    
    .toc-container li a { 
        color: #57606a; 
        font-size: 14px; 
        display: block; 
        padding: 6px 0; 
        text-decoration: none;
        transition: color 0.1s;
    }
    
    .toc-container li a:hover { 
        color: #0969da; 
        font-weight: 600;
    }
    
    /* Main Content Area */
    .content-wrapper { 
        margin-left: 320px; 
        width: calc(100% - 320px);
        display: flex;
        justify-content: center;
    }
    
    .content { 
        padding: 60px 40px; 
        width: 100%; 
        max-width: 900px; 
        line-height: 1.7; 
        font-size: 16px;
    }
    
    pre { 
        background: #f6f8fa; 
        padding: 20px; 
        border-radius: 8px; 
        overflow-x: auto; 
        border: 1px solid #d0d7de;
    }
    
    code { 
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; 
        background: #f6f8fa; 
        padding: 0.2em 0.4em; 
        border-radius: 6px; 
        font-size: 85%;
    }
    
    h1, h2, h3 { 
        color: #1f2328; 
        border-bottom: 1px solid #d0d7de; 
        padding-bottom: 10px; 
        margin-top: 48px;
    }
    
    h1 { border-bottom: 0; margin-top: 0; padding-bottom: 0; font-size: 2.5em; }
    
    a { color: #0969da; text-decoration: none; }
    a:hover { text-decoration: underline; }
    
    table { 
        width: 100%; 
        border-collapse: collapse; 
        margin-top: 24px; 
        margin-bottom: 24px;
    }
    
    th, td { 
        border: 1px solid #d0d7de; 
        padding: 12px 16px; 
        text-align: left; 
    }
    
    th { 
        background: #f6f8fa; 
        font-weight: 600;
    }
    
    blockquote {
        margin: 0;
        padding: 0 1em;
        color: #57606a;
        border-left: 0.25em solid #d0d7de;
    }
</style>
"""

# Initialize markdown compiler with Table of Contents auto-generator enabled!
md = markdown.Markdown(extensions=['toc', 'extra', 'fenced_code', 'tables'])

# Strip [TOC] if it accidentally exists in the text
html_content = md.convert(md_text.replace("[TOC]", ""))
html_toc = md.toc

# Combine everything into one perfectly formatted HTML document
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ReadsClassification Documentation</title>
    {css}
</head>
<body>
    <div class="toc-container">
        <h3>Contents</h3>
        {html_toc}
    </div>
    <div class="content-wrapper">
        <div class="content">
            {html_content}
        </div>
    </div>
</body>
</html>
"""

with open("README.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("✔ Successfully saved README.html with beautiful Sidebar TOC!")
