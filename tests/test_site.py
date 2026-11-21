import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build import ROOT, SITE, app_cards

OUTPUT = ROOT / "_site"


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.language = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append(attrs[name])


class BuiltSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {
            path.relative_to(OUTPUT).as_posix(): Document(path)
            for path in OUTPUT.rglob("*.html")
        }

    def test_each_language_has_main_legal_and_error_pages(self):
        for prefix, language, address in (
            ("", "ko", "경기도 고양시 덕양구 화신로 33"),
            ("en/", "en", "33 Hwasin-ro, Deogyang-gu, Goyang-si, Gyeonggi-do, Republic of Korea"),
        ):
            for name in ("index.html", "privacy/index.html", "terms/index.html", "404.html"):
                with self.subTest(page=prefix + name):
                    self.assertEqual(self.pages[prefix + name].language, language)
            home = (OUTPUT / prefix / "index.html").read_text(encoding="utf-8")
            self.assertIn(address, home)
            self.assertIn("mailto:centumnova@gmail.com", home)

    def test_internal_links_and_fragments_resolve(self):
        for page, document in self.pages.items():
            for link in document.links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(page=page, link=link):
                    target = unquote(url.path).lstrip("/") if url.path else page
                    if url.path.endswith("/"):
                        target += "index.html"
                    self.assertTrue((OUTPUT / target).is_file())
                    if url.fragment:
                        self.assertIn(url.fragment, self.pages[target].ids)

    def test_sitemap_lists_only_canonical_pages(self):
        sitemap = ET.parse(OUTPUT / "sitemap.xml")
        locations = {element.text for element in sitemap.iterfind(".//{*}loc")}
        expected = {SITE + path for path in ("/", "/en/", "/privacy/", "/en/privacy/", "/terms/", "/en/terms/")}
        self.assertEqual(locations, expected)
        for location in locations:
            path = Path(urlsplit(location).path.lstrip("/")) / "index.html"
            self.assertIn(f'href="{location}"', (OUTPUT / path).read_text(encoding="utf-8"))
        self.assertIn(SITE + "/sitemap.xml", (OUTPUT / "robots.txt").read_text(encoding="utf-8"))

    def test_apps_show_play_links_only_when_released(self):
        app = {
            "name": {"en": "Test <app>"},
            "description": {"en": "Test description"},
            "status": "planned",
            "google_play": "https://play.google.com/store/apps/details?id=com.example.app",
            "privacy": {"en": "/en/privacy/"},
        }
        planned = app_cards([app], "en")
        self.assertNotIn("play.google.com", planned)
        self.assertIn("Test &lt;app&gt;", planned)
        self.assertIn('href="/en/privacy/"', planned)
        app["status"] = "released"
        self.assertIn("play.google.com", app_cards([app], "en"))
        app["google_play"] = "javascript:alert(1)"
        with self.assertRaises(ValueError):
            app_cards([app], "en")
