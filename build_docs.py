import markdown
import os

# Read the markdown file
with open("README.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Define modern Apple/GitHub style CSS
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --sidebar-bg: rgba(15, 23, 42, 0.65);
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --accent-glow: #38bdf8;
        --gradient-text: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        --gradient-shimmer: linear-gradient(90deg, #38bdf8, #c084fc, #38bdf8);
        --code-bg: #0b1120;
        --border-color: rgba(255, 255, 255, 0.1);
    }

    body { 
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; 
        display: flex; 
        margin: 0; 
        color: var(--text-main); 
        background-color: var(--bg-color);
        /* Animated Background Gradients! */
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0f172a, #020617);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; border: 2px solid transparent; background-clip: padding-box; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.5); border: 2px solid transparent; background-clip: padding-box; }
    
    /* Hover Glow Navigation Menu */
    .toc-container { 
        width: 360px; 
        position: fixed; 
        height: 100vh; 
        overflow-y: auto; 
        padding: 50px 40px; 
        box-sizing: border-box;
        border-right: 1px solid var(--border-color); 
        background: var(--sidebar-bg); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        z-index: 100;
        box-shadow: 10px 0 30px rgba(0,0,0,0.3);
    }
    
    .toc-container h3 {
        margin-top: 0;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 800;
        margin-bottom: 30px;
        background: var(--gradient-text);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .toc-container ul { list-style: none; padding-left: 20px; margin: 0; border-left: 1px solid var(--border-color); }
    .toc-container > div > ul { padding-left: 0; border-left: none; }
    
    .toc-container li a { 
        color: var(--text-muted); 
        font-size: 15px; 
        display: block; 
        padding: 10px 16px; 
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        margin-bottom: 4px;
        position: relative;
    }
    
    .toc-container li a::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        background: var(--accent-glow);
        border-radius: 50%;
        transition: all 0.3s ease;
        opacity: 0;
    }
    
    .toc-container li a:hover { 
        color: #fff; 
        background: rgba(56, 189, 248, 0.1);
        transform: translateX(6px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
    }
    
    .toc-container li a:hover::before {
        width: 6px;
        height: 6px;
        left: -12px;
        opacity: 1;
        box-shadow: 0 0 10px var(--accent-glow);
    }
    
    /* JavaScript Interactive Active Link States */
    .active-toc-link {
        color: #f8fafc !important;
        background: rgba(56, 189, 248, 0.2) !important;
        font-weight: 800;
        border-right: 4px solid var(--accent-glow);
        transform: scale(1.02);
        box-shadow: inset 20px 0 30px -20px rgba(56, 189, 248, 0.3);
    }
    
    /* Main Content Area */
    .content-wrapper { 
        margin-left: 360px; 
        width: calc(100% - 360px);
        display: flex;
        justify-content: center;
        padding: 60px;
        box-sizing: border-box;
    }
    
    /* Frosted Glass Floating Card */
    .content { 
        padding: 70px 80px; 
        width: 100%; 
        max-width: 1000px; 
        line-height: 1.8; 
        font-size: 17px;
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-color);
        border-radius: 24px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(56, 189, 248, 0.1);
    }
    
    /* Beautiful Markdown Elements */
    pre { 
        background: var(--code-bg); 
        padding: 24px; 
        border-radius: 12px; 
        overflow-x: auto; 
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.5);
    }
    
    code { 
        font-family: 'JetBrains Mono', monospace; 
        background: rgba(148, 163, 184, 0.15); 
        padding: 0.25em 0.5em; 
        border-radius: 6px; 
        font-size: 0.9em;
        color: #f8fafc;
    }
    pre code { background: transparent; border: none; padding: 0; font-size: 14.5px; color: #38bdf8; }
    
    h1, h2, h3, h4 { 
        color: #fff; 
        font-weight: 800;
        margin-top: 2.5em;
        margin-bottom: 24px;
        letter-spacing: -0.5px;
    }
    
    /* Shimmering Animated H1 Title! */
    h1 { 
        font-size: 3.5em; 
        margin-top: 0;
        background: var(--gradient-shimmer);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 5s linear infinite;
        border-bottom: none;
    }
    
    h2 { 
        font-size: 2.2em; 
        border-bottom: 2px solid rgba(255,255,255,0.05); 
        padding-bottom: 0.5em; 
        position: relative;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: var(--accent-glow);
        border-radius: 2px;
        box-shadow: 0 0 10px var(--accent-glow);
    }
    
    a { 
        color: var(--accent-glow); 
        text-decoration: none; 
        position: relative;
        font-weight: 600;
    }
    
    a::after {
        content: '';
        position: absolute;
        width: 100%;
        transform: scaleX(0);
        height: 2px;
        bottom: -2px;
        left: 0;
        background-color: var(--accent-glow);
        transform-origin: bottom right;
        transition: transform 0.3s ease-out;
    }
    
    a:hover::after {
        transform: scaleX(1);
        transform-origin: bottom left;
    }
    
    table { 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 0;
        margin: 3em 0; 
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
        background: rgba(0,0,0,0.2);
    }
    
    th, td { 
        padding: 18px 24px; 
        text-align: left; 
        border-bottom: 1px solid var(--border-color);
    }
    
    th { 
        background: rgba(255,255,255,0.05); 
        font-weight: 800;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 1px;
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(56, 189, 248, 0.05); }
    
    blockquote {
        margin: 2.5em 0;
        padding: 1.5em 2em;
        color: #cbd5e1;
        border-left: 4px solid var(--accent-glow);
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.1) 0%, transparent 100%);
        border-radius: 0 12px 12px 0;
        font-style: italic;
        box-shadow: inset 20px 0 30px -20px rgba(56, 189, 248, 0.15);
    }
    
    img {
        max-width: 100%;
        height: auto !important;
        object-fit: contain;
        display: block;
        margin: 1.5em auto;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    
    img:hover {
        transform: scale(1.02);
    }
    
    iframe {
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.1);
        background: #ffffff; 
        margin-top: 1.5em;
        transition: box-shadow 0.3s ease;
        width: 100%;
        min-height: 850px;
        border: none;
    }
    
    iframe:hover {
        box-shadow: 0 30px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(56, 189, 248, 0.5);
    }
    
    hr {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        border: none;
        margin: 4em 0;
    }
    
    /* Interactive Single-Page App Dynamic CSS */
    .doc-section {
        display: none;
        animation: fadeInSlide 0.5s ease-out forwards;
        min-height: 400px;
    }
    
    .nav-buttons-container {
        display: flex;
        justify-content: space-between;
        margin-top: 60px;
        padding-top: 30px;
        border-top: 1px solid var(--border-color);
    }
    
    .nav-btn {
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--border-color);
        color: var(--text-main);
        padding: 14px 28px;
        border-radius: 10px;
        font-family: inherit;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .nav-btn:hover {
        background: var(--accent-glow);
        color: #0f172a;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(56,189,248,0.3);
    }
</style>
"""

# Initialize markdown compiler with Table of Contents auto-generator enabled!
md = markdown.Markdown(extensions=['toc', 'extra', 'fenced_code', 'tables'])

# Strip [TOC] if it accidentally exists in the text
html_content = md.convert(md_text.replace("[TOC]", ""))
html_toc = md.toc

js_app = """
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const contentDiv = document.querySelector('.content');
        const childrenList = Array.from(contentDiv.children);
        
        const sections = [];
        let currentSectionBox = null;
        let activeIdx = 0;
        
        // 1. Walk the DOM and wrap everything strictly into grouped <section> blocks split by H1/H2
        childrenList.forEach(el => {
            if (el.tagName === 'H1' || el.tagName === 'H2') {
                currentSectionBox = document.createElement('div');
                currentSectionBox.className = 'doc-section';
                currentSectionBox.id = 'sec_' + el.id;
                contentDiv.insertBefore(currentSectionBox, el);
                sections.push({ id: el.id, box: currentSectionBox, title: el.innerText });
            }
            if (currentSectionBox) {
                currentSectionBox.appendChild(el);
            }
        });
        
        // If the top elements don't have an H1/H2, wrap them into a top catch-all box
        contentDiv.childNodes.forEach(node => {
            if (node.nodeType === 1 && node.className !== 'doc-section') {
                if (sections.length > 0) sections[0].box.insertBefore(node, sections[0].box.firstChild);
            }
        });

        // 2. Inject Next & Back Buttons
        sections.forEach((sec, idx) => {
            const footer = document.createElement('div');
            footer.className = 'nav-buttons-container';
            
            const backBtn = document.createElement('button');
            backBtn.className = 'nav-btn';
            if (idx > 0) {
                backBtn.innerHTML = `&larr; Back<br><span style="font-size:12px;opacity:0.7">` + sections[idx-1].title + `</span>`;
                backBtn.onclick = () => switchSection(idx - 1);
            } else {
                backBtn.style.visibility = 'hidden';
            }
            
            const nextBtn = document.createElement('button');
            nextBtn.className = 'nav-btn';
            if (idx < sections.length - 1) {
                nextBtn.innerHTML = `Next &rarr;<br><span style="font-size:12px;opacity:0.7">` + sections[idx+1].title + `</span>`;
                nextBtn.onclick = () => switchSection(idx + 1);
            } else {
                nextBtn.style.visibility = 'hidden';
            }
            
            footer.appendChild(backBtn);
            footer.appendChild(nextBtn);
            sec.box.appendChild(footer);
        });

        // 3. Section Switcher Logic
        window.switchSection = (idx) => {
            sections.forEach(s => s.box.style.display = 'none');
            document.querySelectorAll('.toc-container a').forEach(a => a.classList.remove('active-toc-link'));
            
            sections[idx].box.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Force Plotly iframes to mathematically recalculate canvas scaling 
            // by physically reloading the iframe src after the parent container is visible!
            const iframes = sections[idx].box.querySelectorAll('iframe');
            iframes.forEach(ifr => {
                const src = ifr.getAttribute('src');
                ifr.setAttribute('src', src);
            });
            
            // Add Glow to specific Table of Contents Link
            const activeLink = document.querySelector(`.toc-container a[href="#${sections[idx].id}"]`);
            if (activeLink) {
                activeLink.classList.add('active-toc-link');
                activeLink.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        };

        // 4. Overwrite Links in Table of Contents to intercept scrolling
        document.querySelectorAll('.toc-container a').forEach(link => {
            link.addEventListener('click', (e) => {
                const hrefId = link.getAttribute('href').substring(1);
                
                // Find matching header ID inside our sections
                const targetHeader = document.getElementById(hrefId);
                if (targetHeader) {
                    const parentSec = targetHeader.closest('.doc-section');
                    if (parentSec) {
                        e.preventDefault();
                        const findIdx = sections.findIndex(s => s.box === parentSec);
                        if (findIdx !== -1) {
                            switchSection(findIdx);
                            // Only scroll if we clicked a subsection (H3, H4)
                            if (targetHeader.tagName !== 'H1' && targetHeader.tagName !== 'H2') {
                                setTimeout(() => targetHeader.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
                            }
                        }
                    }
                }
            });
        });

        // Init App Interface
        if (sections.length > 0) switchSection(0);
    });
</script>
"""

# Combine everything into one perfectly formatted HTML document
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ReadsClassification Interactive Documentation</title>
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
    
    <!-- Reactivity JS Engine -->
    {js_app}
    
</body>
</html>
"""

with open("README.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("✔ Successfully engineered interactive Single Page Application build!")
