import markdown
import os

# Read the markdown file
with open("README.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Define modern Apple/GitHub style CSS
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;500&display=swap');
    
    :root {
        --bg-color: #0d1117;
        --sidebar-bg: rgba(13, 17, 23, 0.85);
        --text-main: #c9d1d9;
        --text-muted: #8b949e;
        --accent-color: #58a6ff;
        --accent-gradient: linear-gradient(135deg, #58a6ff 0%, #3fb950 100%);
        --code-bg: #161b22;
        --border-color: #30363d;
        --card-bg: #1c2128;
    }

    body { 
        font-family: 'Outfit', -apple-system, sans-serif; 
        display: flex; 
        margin: 0; 
        color: var(--text-main); 
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,0.1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,0.1) 0, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Sleek Webkit Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    
    /* Left side Glassmorphism TOC */
    .toc-container { 
        width: 340px; 
        position: fixed; 
        height: 100vh; 
        overflow-y: auto; 
        padding: 40px 30px; 
        box-sizing: border-box;
        border-right: 1px solid var(--border-color); 
        background: var(--sidebar-bg); 
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 100;
    }
    
    .toc-container h3 {
        margin-top: 0;
        font-size: 14px;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 800;
        margin-bottom: 24px;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .toc-container ul { list-style: none; padding-left: 16px; margin: 0; }
    .toc-container > div > ul { padding-left: 0; }
    
    .toc-container li a { 
        color: var(--text-muted); 
        font-size: 15px; 
        display: block; 
        padding: 8px 12px; 
        text-decoration: none;
        border-radius: 6px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2px;
    }
    
    .toc-container li a:hover { 
        color: #fff; 
        background: rgba(88, 166, 255, 0.1);
        transform: translateX(4px);
    }
    
    /* Main Content Area */
    .content-wrapper { 
        margin-left: 340px; 
        width: calc(100% - 340px);
        display: flex;
        justify-content: center;
    }
    
    .content { 
        padding: 60px 40px; 
        width: 100%; 
        max-width: 950px; 
        line-height: 1.8; 
        font-size: 17px;
    }
    
    /* Beautiful Markdown Elements */
    pre { 
        background: var(--code-bg); 
        padding: 24px; 
        border-radius: 12px; 
        overflow-x: auto; 
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    code { 
        font-family: 'Fira Code', monospace; 
        background: rgba(110, 118, 129, 0.2); 
        padding: 0.2em 0.4em; 
        border-radius: 6px; 
        font-size: 85%;
        color: #e6edf3;
    }
    pre code { background: transparent; border: none; padding: 0; font-size: 14px; }
    
    h1, h2, h3, h4 { 
        color: #fff; 
        font-weight: 600;
        margin-top: 2em;
        margin-bottom: 16px;
    }
    
    h1 { 
        font-size: 3em; 
        font-weight: 800;
        margin-top: 0;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    h2 { font-size: 2em; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }
    
    a { color: var(--accent-color); text-decoration: none; transition: color 0.2s; }
    a:hover { color: #79c0ff; text-decoration: underline; }
    
    table { 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 0;
        margin: 2em 0; 
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    th, td { 
        padding: 16px; 
        text-align: left; 
        border-bottom: 1px solid var(--border-color);
    }
    
    th { 
        background: var(--card-bg); 
        font-weight: 600;
        color: #fff;
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255,255,255,0.02); }
    
    blockquote {
        margin: 2em 0;
        padding: 1em 1.5em;
        color: var(--text-muted);
        border-left: 4px solid var(--accent-color);
        background: var(--card-bg);
        border-radius: 0 8px 8px 0;
    }
    
    img {
        max-width: 100%;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    iframe {
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        background: #fff; 
        margin-top: 1em;
    }
    
    hr {
        height: 1px;
        background: var(--border-color);
        border: none;
        margin: 3em 0;
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
