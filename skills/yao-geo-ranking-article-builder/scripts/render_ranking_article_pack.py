#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-ranking-article-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

from __future__ import annotations
import argparse, html, re, shutil, subprocess, zipfile
from pathlib import Path
import markdown
from weasyprint import HTML
CSS=""":root{color-scheme:light;--ink:#1f2933;--line:#d7dde5;--soft:#f4f6f8;--accent:#0f766e}*{box-sizing:border-box}html,body{margin:0;padding:0;background:#fff;color:var(--ink)}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans CJK SC","Microsoft YaHei","PingFang SC",Arial,sans-serif;font-size:15px;line-height:1.78}.report{max-width:1040px;margin:0 auto;padding:34px 30px 60px}h1,h2,h3{color:#111827;line-height:1.28;margin:1.35em 0 .55em;letter-spacing:0}h1{font-size:30px;margin-top:0;padding-bottom:16px;border-bottom:2px solid #111827}h2{font-size:22px;padding-top:6px}h3{font-size:17px}p{margin:0 0 12px}a{color:var(--accent);text-decoration:none;overflow-wrap:anywhere}.table-wrap{width:100%;overflow-x:auto;margin:14px 0 22px}table{width:100%;border-collapse:collapse;table-layout:fixed;background:#fff}th,td{border:1px solid var(--line);padding:10px 12px;vertical-align:top;overflow-wrap:anywhere;word-break:break-word}th{background:var(--soft);font-weight:700;color:#111827}@page{size:A4;margin:18mm 16mm}@media print{body{background:#fff}.report{max-width:none;padding:0}h2,h3{break-after:avoid}tr{break-inside:avoid;page-break-inside:avoid}}"""
def slugify(v): return re.sub(r'-+','-',re.sub(r'[^a-z0-9\u4e00-\u9fff-]+','-',v.strip().lower())).strip('-') or 'geo-ranking-article'
def md_to_html(txt): return re.sub(r'(<table>.*?</table>)',r'<div class="table-wrap">\1</div>',markdown.markdown(txt,extensions=['extra','tables','sane_lists'],output_format='html5'),flags=re.S)
def build_html(title,txt): return f'<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head><body><main class="report">{md_to_html(txt)}</main></body></html>'
def ux(s): return s.replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'").replace('&amp;','&')
def ex(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&apos;')
def soft(raw): return re.sub(r'([/._?=&%+-])', lambda m: m.group(1)+'​', raw)
def soft_breaks(doc):
    def r(m):
        raw=ux(m.group(1))
        return '<w:t>'+ex(soft(raw))+'</w:t>' if len(raw)>=16 and re.search(r'https?://|[A-Za-z0-9][A-Za-z0-9_./?=&%+-]{15,}',raw) else m.group(0)
    return re.sub(r'<w:t>(.*?)</w:t>',r,doc,flags=re.S)
def score(v):
    v=re.sub(r'\s+','',v); sc=sum(1 if '一'<=ch<='鿿' else (.62 if ch.isascii() and ch.isalnum() else .35) for ch in v)
    return sc*1.35 if re.search(r'https?://|[A-Za-z0-9][A-Za-z0-9_./?=&%+-]{18,}',v) else sc
def cell_text(x): return ''.join(ux(t) for t in re.findall(r'<w:t[^>]*>(.*?)</w:t>',x,flags=re.S))
def widths(tbl,total=10466):
    rows=re.findall(r'<w:tr>.*?</w:tr>',tbl,flags=re.S); first=re.findall(r'<w:tc>.*?</w:tc>',rows[0],flags=re.S) if rows else []; n=len(first)
    if not n: return []
    vals=[1.0]*n
    for row in rows:
        for i,c in enumerate(re.findall(r'<w:tc>.*?</w:tc>',row,flags=re.S)[:n]): vals[i]+=min(score(cell_text(c)),80)**.72
    mn=900 if n>=4 else 1100; avail=total-mn*n
    if avail<=0: return [total//n]*n
    out=[mn+int(avail*v/sum(vals)) for v in vals]; diff=total-sum(out); i=0
    while diff:
        step=1 if diff>0 else -1; j=i%len(out)
        if step>0 or out[j]>mn: out[j]+=step; diff-=step
        i+=1
    return out
def patch_docx(p):
    border='<w:tblBorders><w:top w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/><w:left w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/><w:right w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/><w:insideH w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/><w:insideV w:val="single" w:sz="6" w:space="0" w:color="D7DDE5"/></w:tblBorders>'
    mar='<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'
    with zipfile.ZipFile(p) as z: ent={n:z.read(n) for n in z.namelist()}
    doc=ent['word/document.xml'].decode(); page='<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="900" w:right="720" w:bottom="900" w:left="720" w:header="360" w:footer="360" w:gutter="0"/>'
    doc=re.sub(r'<w:sectPr\b[^>]*>.*?</w:sectPr>',lambda m: re.sub(r'<w:pgSz\b[^>]*/>|<w:pgMar\b[^>]*/>','',m.group(0)).replace('>', '>'+page,1),doc,flags=re.S); doc=soft_breaks(doc)
    def tr(m):
        tbl=m.group(0); ws=widths(tbl)
        if not ws: return tbl
        grid='<w:tblGrid>'+''.join(f'<w:gridCol w:w="{x}"/>' for x in ws)+'</w:tblGrid>'
        tbl=re.sub(r'<w:tblGrid>.*?</w:tblGrid>',grid,tbl,count=1,flags=re.S) if '<w:tblGrid>' in tbl else tbl.replace('</w:tblPr>','</w:tblPr>'+grid,1)
        idx={'v':0}
        def cr(c):
            width=ws[idx['v']%len(ws)]; idx['v']+=1; cell=re.sub(r'<w:tcW\b[^>]*/>','',c.group(0)); return cell.replace('<w:tcPr>',f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:vAlign w:val="top"/>',1)
        tbl=re.sub(r'<w:tc>.*?</w:tc>',cr,tbl,flags=re.S)
        def pr(pm):
            props=re.sub(r'<w:tblBorders>.*?</w:tblBorders>|<w:tblCellMar>.*?</w:tblCellMar>','',pm.group(1),flags=re.S); props=re.sub(r'<w:tblW\b[^>]*/>|<w:tblLayout\b[^>]*/>|<w:jc\b[^>]*/>|<w:tblInd\b[^>]*/>','',props)
            return '<w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'+props+border+mar+'</w:tblPr>'
        return re.sub(r'<w:tblPr>(.*?)</w:tblPr>',pr,tbl,count=1,flags=re.S)
    doc=re.sub(r'<w:tbl>.*?</w:tbl>',tr,doc,flags=re.S); ent['word/document.xml']=doc.encode(); tmp=p.with_suffix('.tmp.docx')
    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
        for n,d in ent.items(): z.writestr(n,d)
    tmp.replace(p)
def write_docx(md,docx):
    if not shutil.which('pandoc'): raise RuntimeError('pandoc missing')
    subprocess.run(['pandoc',str(md),'-o',str(docx),'--standalone'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True); patch_docx(docx)
def check(out,slug,h):
    for s in ['.md','.html','.pdf','.docx']:
        p=out/f'{slug}{s}'; assert p.is_file() and p.stat().st_size>0, p
    for n in ['background:#fff','line-height:1.78','border-collapse:collapse','overflow-wrap:anywhere','@page{size:A4']: assert n in h, n
    with zipfile.ZipFile(out/f'{slug}.docx') as z: doc=z.read('word/document.xml').decode()
    for tbl in re.findall(r'<w:tbl>.*?</w:tbl>',doc,flags=re.S):
        ws=[int(x) for x in re.findall(r'<w:gridCol w:w="(\d+)"',tbl)]; assert ws and sum(ws)<=10466; assert '<w:tblLayout w:type="fixed"' in tbl
    assert doc.count('<w:tblBorders>')>=doc.count('<w:tbl>')>0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--output-dir',type=Path,required=True); ap.add_argument('--slug',default=''); ap.add_argument('--title',default=''); a=ap.parse_args(); a.output_dir.mkdir(parents=True,exist_ok=True)
    txt=a.source.read_text(encoding='utf-8'); title=a.title or re.search(r'^#\s+(.+)$',txt,re.M).group(1); slug=slugify(a.slug or a.source.stem)
    md=a.output_dir/f'{slug}.md'; hp=a.output_dir/f'{slug}.html'; pdf=a.output_dir/f'{slug}.pdf'; docx=a.output_dir/f'{slug}.docx'; md.write_text(txt,encoding='utf-8'); h=build_html(title,txt); hp.write_text(h,encoding='utf-8'); HTML(string=h,base_url=str(a.output_dir)).write_pdf(str(pdf)); write_docx(md,docx); (a.output_dir/'index.html').write_text(build_html(title+' - 文章包',f'# {title} - 文章包\n\n- [Markdown]({slug}.md)\n- [HTML]({slug}.html)\n- [PDF]({slug}.pdf)\n- [Word]({slug}.docx)'),encoding='utf-8'); check(a.output_dir,slug,h); [print('generated:',p) for p in [md,hp,pdf,docx,a.output_dir/'index.html']]
if __name__=='__main__': main()
