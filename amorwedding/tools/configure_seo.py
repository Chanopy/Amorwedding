"""Generate static SEO metadata. Run once before deployment; no runtime dependency."""
from pathlib import Path
from urllib.parse import urlsplit
from html import escape
import os
import json
import re

ROOT = Path(__file__).resolve().parent.parent
START, END = '<!-- AMOR SEO START -->', '<!-- AMOR SEO END -->'

def configure(root=ROOT):
    config = json.loads((root / 'seo-config.json').read_text(encoding='utf-8'))
    base = (os.environ.get('SITE_URL') or config['site_url'] or os.environ.get('URL', '')).strip()
    if base:
        parsed = urlsplit(base)
        if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.path not in ('', '/')
                or parsed.port not in (None, 443)):
            raise ValueError('site_url에는 HTTPS 도메인 루트 주소를 입력하세요. 경로·쿼리·인증정보는 사용할 수 없습니다.')
        base = base.rstrip('/') + '/'
    title = '아모르 웨딩 | 웨딩 패키지·웨딩 당일 케어'
    description = '결혼 준비부터 웨딩 당일, 애프터케어까지 함께하는 아모르 웨딩. BASIC·PREMIUM·VIP 웨딩 패키지와 사회자, 축가, 맞춤형 결혼식 진행 음원을 만나보세요. 카카오톡으로 상담하실 수 있습니다.'
    tags = [START, '<title>' + escape(title) + '</title>']
    def meta(key, value, attr='name'):
        tags.append(f'<meta {attr}="{key}" content="{escape(value, quote=True)}">')
    meta('description', description)
    meta('robots', 'index, follow, max-image-preview:large')
    meta('theme-color', '#30382f')
    for k, v in [('type', 'website'), ('locale', 'ko_KR'), ('site_name', '아모르 웨딩'), ('title', title), ('description', description)]:
        meta('og:' + k, v, 'property')
    meta('twitter:card', 'summary_large_image')
    meta('og:image', base + 'assets/og-amor.jpg', 'property')
    meta('og:image:type', 'image/jpeg', 'property')
    meta('og:image:width', '1200', 'property')
    meta('og:image:height', '630', 'property')
    meta('og:image:alt', '아모르 웨딩 AMOR 로고', 'property')
    meta('twitter:image', base + 'assets/og-amor.jpg')
    meta('twitter:image:alt', '아모르 웨딩 AMOR 로고')
    meta('twitter:title', title)
    meta('twitter:description', description)
    org = {'@type': 'Organization', '@id': base + '#organization', 'name': '아모르 웨딩',
           'alternateName': 'AMOR WEDDING', 'description': '상담·설계·실행·웨딩 당일·애프터케어를 함께하는 웨딩 토탈케어 파트너',
           'sameAs': ['https://pf.kakao.com/_SKRMX'], 'telephone': '+82-10-8214-6334', 'taxID': '690-32-01797', 'address': {'@type':'PostalAddress','streetAddress':'단원구 원초로 9, 811-505','addressLocality':'안산시','addressRegion':'경기도','addressCountry':'KR'}}
    service = {'@type': 'Service', 'name': '아모르 웨딩 토탈케어', 'serviceType': '웨딩 패키지 및 결혼 준비 상담',
               'provider': {'@id': base + '#organization'},
               'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': '웨딩 패키지', 'itemListElement': []}}
    descriptions = {
        'BASIC': '웨딩케어(당일케어), 청첩장, 답례품, 축가(1인), 사회자',
        'PREMIUM': '웨딩케어(당일케어), 청첩장, 답례품, 축가(3~4인), 사회자, 픽업서비스, 맞춤형 결혼식 진행 음원',
        'VIP': '웨딩케어(당일케어), 청첩장·식권·답례품, 맞춤형 축가(4~6인), 맞춤형 오프닝곡, 사회자, 축의대, 픽업서비스, 맞춤형 결혼식 진행 음원'}
    for name, desc in descriptions.items():
        service['hasOfferCatalog']['itemListElement'].append({'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': name + ' 웨딩 패키지', 'description': desc}})
    graph = [org, service]
    if base:
        tags.append(f'<link rel="canonical" href="{escape(base, quote=True)}">')
        meta('og:url', base, 'property')
        org.update(url=base, logo=base + 'assets/AMOR_logo_black_textured.png')
        service['url'] = base + '#packages'
        graph.append({'@type': 'WebSite', '@id': base + '#website', 'url': base, 'name': '아모르 웨딩', 'alternateName': 'AMOR WEDDING', 'inLanguage': 'ko-KR', 'publisher': {'@id': base + '#organization'}})
    for key in ['naver-site-verification', 'google-site-verification']:
        token = config.get(key, '').strip()
        if token:
            meta(key, token)
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    tags += ['<script type="application/ld+json">\n' + data + '\n</script>', END]
    path = root / 'index.html'
    html = path.read_text(encoding='utf-8')
    if START in html:
        html = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: '\n'.join(tags), html, flags=re.S)
    else:
        html = re.sub(r'<title>.*?</title>\s*<meta name="description"[^>]*>', lambda _: '\n'.join(tags), html, count=1, flags=re.S)
    path.write_text(html, encoding='utf-8')
    robots = 'User-agent: *\nAllow: /\n'
    if base:
        robots += '\nSitemap: ' + base + 'sitemap.xml\n'
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>' + escape(base) + '</loc></url>\n</urlset>\n'
        (root / 'sitemap.xml').write_text(xml, encoding='utf-8')
    else:
        (root / 'sitemap.xml').unlink(missing_ok=True)
    (root / 'robots.txt').write_text(robots, encoding='utf-8')
    print('SEO 생성 완료: ' + (base if base else '도메인 미정 — canonical, 공유 이미지 URL, sitemap.xml은 도메인 입력 후 생성됩니다.'))

if __name__ == '__main__':
    configure()
