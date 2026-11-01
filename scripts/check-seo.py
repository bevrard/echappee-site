"""Contrôle la cohérence des signaux SEO du site statique, sans dépendance."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.canonicals = []
        self.ids = set()
        self.anchors = []
        self.images = []
        self.title = ''
        self.h1 = ''
        self.schema = ''
        self.current = None
        self.in_main = False
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            assert attrs.get('lang') == 'fr', 'Langue française manquante'
        if tag == 'main':
            self.in_main = True
        if tag in ('title', 'h1'):
            self.current = tag
        if tag == 'h1':
            self.h1_count += 1
            assert self.in_main, 'Le H1 doit appartenir au contenu principal'
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.current = 'schema'
        if tag == 'meta':
            key = attrs.get('name') or attrs.get('property')
            assert key not in self.meta, f'Métadonnée dupliquée : {key}'
            self.meta[key] = attrs.get('content')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        if tag == 'img':
            self.images.append(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])

    def handle_endtag(self, tag):
        if tag in ('title', 'h1', 'script'):
            self.current = None
        if tag == 'main':
            self.in_main = False

    def handle_data(self, data):
        if self.current:
            setattr(self, self.current, getattr(self, self.current) + data)


page = Page()
page.feed((ROOT / 'index.html').read_text())
canonical = 'https://' + (ROOT / 'CNAME').read_text().strip() + '/'
assert page.canonicals == [canonical], 'URL canonique différente du domaine Pages'
assert page.h1_count == 1 and page.h1.strip(), 'Un seul H1 est attendu'
assert page.title.strip() and page.meta['description'].strip()
assert not any(value in (page.meta.get('robots') or '').lower() for value in ('noindex', 'nofollow'))
assert page.meta['og:url'] == canonical
assert page.meta['og:type'] == 'website'
for prefix in ('og', 'twitter'):
    assert page.meta[f'{prefix}:title'] == page.title
    assert page.meta[f'{prefix}:description'] == page.meta['description']
    image = page.meta[f'{prefix}:image']
    assert image.startswith(canonical), 'Image de partage hors du domaine canonique'
    assert (ROOT / urlsplit(image).path.lstrip('/')).is_file()
    assert page.meta[f'{prefix}:image:alt'].strip()
assert page.meta['twitter:card'] == 'summary'
for image in page.images:
    assert 'alt' in image
    assert int(image['width']) > 0 and int(image['height']) > 0
    assert (ROOT / image['src']).is_file()
assert set(page.anchors) <= page.ids, 'Ancre interne inexistante'
schema = json.loads(page.schema)
assert schema['@context'] == 'https://schema.org'
website, webpage = schema['@graph']
assert website['@type'] == 'WebSite' and webpage['@type'] == 'WebPage'
assert website['url'] == webpage['url'] == canonical
assert webpage['isPartOf']['@id'] == website['@id']
assert webpage['name'] == page.title
assert webpage['description'] == page.meta['description']
assert webpage['primaryImageOfPage']['url'] == page.meta['og:image']
sitemap = ET.parse(ROOT / 'sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert [loc.text for loc in sitemap.findall('s:url/s:loc', ns)] == [canonical]
robots = RobotFileParser()
robots.parse((ROOT / 'robots.txt').read_text().splitlines())
assert robots.site_maps() == [canonical + 'sitemap.xml']
for agent in ('Googlebot', 'Bingbot', '*'):
    for path in ('', 'assets/rouleur-logo.png', 'sitemap.xml'):
        assert robots.can_fetch(agent, canonical + path), f'Exploration bloquée : {path}'
print('SEO vérifié : métadonnées, URL canonique, partage, JSON-LD, sitemap et robots.txt.')
