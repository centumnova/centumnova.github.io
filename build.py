"""Build the bilingual CENTUMNOVA website with Python's standard library."""
import argparse
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SITE = "https://centumnova.github.io"
EMAIL = "centumnova@gmail.com"
BRAND = "CENTUMNOVA"
LANGUAGES = ("ko", "en")
PAGES = {"home": "", "privacy": "privacy/", "terms": "terms/", "404": "404.html"}

COPY = {
    "ko": {
        "name": "센텀노바", "representative": "대표 나수연",
        "address": "경기도 고양시 덕양구 화신로 33",
        "slogan": "당신의 일상에\n새로운 가능성을",
        "description": "센텀노바는 교육과 업무, 일상과 여가를 위한 소프트웨어와 디지털 서비스를 개발합니다.",
        "intro": "배움과 일, 그리고 즐거움을 위한 소프트웨어.\n센텀노바는 일상에 자연스럽게 스며드는 디지털 경험을 만듭니다.",
        "nav": ("홈", "회사 소개", "사업 분야", "앱", "문의"),
        "about_title": "일상에 가치를 더하는\n소프트웨어를 만듭니다.",
        "about": ("센텀노바는 2026년 대한민국에서 설립된 소프트웨어 개발 사업체입니다. 교육, 업무 생산성, 모바일 애플리케이션, 게임 및 디지털 서비스를 개발합니다.",
                  "사업자등록상 업종은 응용 소프트웨어 개발 및 공급업, 포털 및 기타 인터넷 정보 매개 서비스업입니다."),
        "business_title": "우리가 만드는 것",
        "business_intro": "배움에서 여가까지, 네 가지 분야에서 더 나은 디지털 경험을 만듭니다.",
        "business": ("배움을 더 쉽게 시작하고 꾸준히 이어갈 수 있는 교육용 소프트웨어를 개발합니다.",
                     "반복되는 업무를 줄이고 중요한 일에 집중할 수 있는 도구를 개발합니다.",
                     "일상에서 필요한 기능을 손쉽게 이용할 수 있는 모바일 앱을 개발합니다.",
                     "플레이와 상호작용을 통해 즐거움을 주는 디지털 콘텐츠를 개발합니다."),
        "apps_title": "센텀노바의 앱", "empty": "공개된 앱이 없습니다. 앱 출시 소식은 이곳에서 안내합니다.",
        "status": {"planned": "출시 예정", "development": "개발 중", "released": "출시"},
        "store": "Google Play에서 보기", "contact_title": "센텀노바에 문의하세요",
        "contact_intro": "제품, 협업 및 기타 문의는 공식 이메일로 보내 주세요.",
        "contact_action": "이메일 보내기", "privacy": "개인정보처리방침", "terms": "이용약관",
        "theme": "다크 모드", "skip": "본문 바로가기", "missing": "페이지를 찾을 수 없습니다",
        "missing_body": "홈으로 돌아가 원하는 정보를 찾아보세요.",
        "privacy_sections": (
            ("적용 범위", "이 방침은 센텀노바 공식 홈페이지에 적용됩니다. 앱의 개인정보 처리 방식은 각 앱의 개인정보처리방침에서 안내합니다."),
            ("홈페이지 이용", "홈페이지는 회원가입, 입력 양식, 광고 및 방문 분석 도구를 사용하지 않습니다. 표시 모드 설정은 브라우저의 로컬 저장소에 기록되며, 사이트 기능을 통해 센텀노바로 전송되지 않습니다."),
            ("호스팅", "홈페이지는 GitHub Pages에서 호스팅됩니다. GitHub는 서비스 제공 및 보안을 위해 IP 주소 등 접속 정보를 처리할 수 있습니다."),
            ("이메일 문의", "이메일을 보내면 발신 주소와 본문 등 직접 제공한 정보를 받습니다. 문의를 확인하고 답변하는 데 사용하며, 처리 목적이 달성되면 삭제합니다. 법령상 보존 의무가 있는 경우 해당 기간 동안 보관합니다."),
            ("권리 행사 및 문의", "개인정보의 열람, 정정, 삭제 및 처리 정지를 요청하거나 개인정보 처리에 관해 문의하려면 공식 이메일로 연락해 주세요."),
        ),
        "terms_sections": (
            ("적용 범위", "이 약관은 센텀노바 공식 홈페이지 이용에 적용됩니다. 앱과 외부 서비스에는 해당 서비스의 약관이 적용될 수 있습니다."),
            ("홈페이지의 정보", "홈페이지는 회사 및 제품 정보를 제공합니다. 제품의 출시 일정과 제공 기능은 변경될 수 있습니다."),
            ("콘텐츠 이용", "홈페이지의 콘텐츠에는 관련 법령에 따른 권리가 적용됩니다. 법령이 허용하거나 권리자가 동의한 범위에서 이용할 수 있습니다."),
            ("외부 링크 및 문의", "외부 링크를 이용할 때는 해당 서비스의 약관과 개인정보처리방침을 확인해 주세요. 홈페이지 이용에 관한 문의는 공식 이메일로 보내 주세요."),
        ),
    },
    "en": {
        "name": "CENTUMNOVA", "representative": "Representative: Suyeon Na",
        "address": "33 Hwasin-ro, Deogyang-gu, Goyang-si, Gyeonggi-do, Republic of Korea",
        "slogan": "New Possibilities\nat Your Fingertips",
        "description": "CENTUMNOVA develops software and digital services for learning, work, everyday life, and play.",
        "intro": "Software for learning, work, and play.\nWe build digital experiences that fit into everyday life.",
        "nav": ("Home", "About", "Business", "Apps", "Contact"),
        "about_title": "We build software\nfor everyday life.",
        "about": ("Founded in 2026 in the Republic of Korea, CENTUMNOVA develops software for education and workplace productivity, as well as mobile applications, games, and digital services.",
                  "Our registered business activities are application software development and supply, and portal and other internet information brokerage services."),
        "business_title": "What we build",
        "business_intro": "Four areas of focus, from learning and work to everyday life and play.",
        "business": ("Education software that makes it easier to start learning and keep going.",
                     "Tools that cut down on repetitive work so people can focus on what matters.",
                     "Mobile apps that put useful everyday features within easy reach.",
                     "Games and interactive digital content designed for people to enjoy."),
        "apps_title": "CENTUMNOVA apps", "empty": "No apps are publicly listed yet. Check here for release updates.",
        "status": {"planned": "Coming soon", "development": "In development", "released": "Released"},
        "store": "View on Google Play", "contact_title": "Get in touch with CENTUMNOVA",
        "contact_intro": "Email us for product, collaboration, or general inquiries.",
        "contact_action": "Send an email", "privacy": "Privacy policy", "terms": "Terms of use",
        "theme": "Dark mode", "skip": "Skip to content", "missing": "Page not found",
        "missing_body": "Return to the homepage to find what you were looking for.",
        "privacy_sections": (
            ("Scope", "This policy applies to the CENTUMNOVA website. Each app can provide a separate privacy policy covering how it handles personal data."),
            ("Website use", "This site uses no accounts, web forms, advertising, or traffic analytics. Your display preference is stored in your browser’s local storage. The site does not transmit it to CENTUMNOVA."),
            ("Hosting", "This website is hosted by GitHub Pages. GitHub may process connection information such as IP addresses to provide and secure its service."),
            ("Email inquiries", "When you email us, we receive your address and any details you include. We use that information to review and answer your inquiry, and delete it once that purpose has been fulfilled, subject to legally required retention."),
            ("Your rights and contact", "Email us to request access, correction, deletion, or suspension of processing, or to ask about personal data handling."),
        ),
        "terms_sections": (
            ("Scope", "These terms apply to the CENTUMNOVA website. Apps and external services may have their own terms."),
            ("Website information", "This site provides company and product information. Release schedules and product features may change."),
            ("Use of content", "Website content is subject to applicable intellectual property rights. You may use it as permitted by law or with the rights holder’s consent."),
            ("External links and contact", "Review the applicable terms and privacy policy before using external services. Contact us at our official email address with website inquiries."),
        ),
    },
}

FIELDS = ("Education Technology", "Productivity Tools", "Mobile Applications", "Games & Interactive Content")
ICONS = (
    '<path d="m2 9 10-5 10 5-10 5L2 9Zm4 2v6c4 3 8 3 12 0v-6m4-2v6"/>',
    '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="m8 12 3 3 5-6"/>',
    '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    '<path d="M7 7h10c2 0 3 1 4 4l1 5c0 2-2 3-4 1l-2-2H8l-2 2c-2 2-4 1-4-1l1-5c1-3 2-4 4-4Zm0 4v4m-2-2h4m6 0h.01M18 11h.01"/>',
)
ARROW = '<span aria-hidden="true">↗</span>'
GITHUB_PRIVACY = "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"


def esc(value):
    return html.escape(value, quote=True)


def multiline(value):
    return esc(value).replace("\n", "<br>")


def route(lang, page="home"):
    return ("/" if lang == "ko" else "/en/") + PAGES[page]


def external_link(value, host=None):
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("External app links must use HTTPS without embedded credentials.")
    if host and (url.netloc != host or url.path != "/store/apps/details" or not url.query):
        raise ValueError("Google Play links must point to an app listing.")
    return esc(value)


def privacy_link(value):
    if re.fullmatch(r"/(?:[\w.-]+/)*[\w.-]*", value) and not any(
        part in {".", ".."} for part in value.split("/")
    ):
        return esc(value)
    return external_link(value)


def app_cards(apps, lang):
    c = COPY[lang]
    if not apps:
        return f'<div class="empty"><span class="empty-icon" aria-hidden="true">✦</span><p>{esc(c["empty"])}</p></div>'
    cards = []
    for app in apps:
        icon = app.get("icon", "/assets/mark.svg")
        if not re.fullmatch(r"/assets/[a-zA-Z0-9][a-zA-Z0-9._/-]*", icon) or ".." in icon:
            raise ValueError("App icons must be local assets.")
        if not (ROOT / icon.lstrip("/")).is_file():
            raise ValueError(f"Missing app icon: {icon}")
        status = app["status"]
        play = app.get("google_play")
        privacy = app.get("privacy", {}).get(lang)
        links = []
        if status == "released" and play:
            links.append(f'<a href="{external_link(play, "play.google.com")}">{esc(c["store"])} {ARROW}</a>')
        if privacy:
            links.append(f'<a href="{privacy_link(privacy)}">{esc(c["privacy"])}</a>')
        cards.append(f'''<article class="card app-card">
          <img src="{esc(icon)}" width="48" height="48" alt="">
          <p class="app-status">{esc(c["status"][status])}</p>
          <h3>{esc(app["name"][lang])}</h3><p>{esc(app["description"][lang])}</p>
          <div class="app-links">{"".join(links)}</div>
        </article>''')
    return f'<div class="card-grid">{"".join(cards)}</div>'


def wordmark():
    return f'<img src="/assets/mark.svg" width="32" height="32" alt=""><span>{esc(BRAND)}</span>'


def layout(lang, page, title, body):
    c = COPY[lang]
    other = "en" if lang == "ko" else "ko"
    alt = route(other, page)
    home = route(lang)
    canonical = SITE + route(lang, page)
    full_title = BRAND if page == "home" else f"{title} | {BRAND}"
    nav_links = []
    for label, anchor in zip(c["nav"], ("", "#about", "#business", "#apps", "#contact")):
        current = ' aria-current="page"' if page == "home" and not anchor else ""
        nav_links.append(f'<a href="{home}{anchor}"{current}>{esc(label)}</a>')
    search = '<meta name="robots" content="noindex">' if page == "404" else f'''
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="ko" href="{SITE + route("ko", page)}">
    <link rel="alternate" hreflang="en" href="{SITE + route("en", page)}">
    <link rel="alternate" hreflang="x-default" href="{SITE + route("ko", page)}">'''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full_title)}</title>
  <meta name="description" content="{esc(c["description"] if page == "home" else f"{title} | {BRAND}")}">
{search}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{esc(BRAND)}">
  <meta property="og:title" content="{esc(full_title)}">
  <meta property="og:description" content="{esc(c["description"] if page == "home" else title)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/social-card.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="CENTUMNOVA — New Possibilities at Your Fingertips">
  <meta property="og:locale" content="{"ko_KR" if lang == "ko" else "en_US"}">
  <!-- Search Console HTML file verification is supported via public/. -->
  <link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
  <script src="/assets/theme.js"></script>
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <a class="skip" href="#main">{esc(c["skip"])}</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="wordmark" href="{home}">{wordmark()}</a>
      <nav aria-label="{"주 메뉴" if lang == "ko" else "Main navigation"}">{"".join(nav_links)}</nav>
      <div class="controls">
        <a class="language" href="{alt}" hreflang="{other}" lang="{other}">{"EN" if other == "en" else "한국어"}</a>
        <button type="button" class="theme" aria-label="{esc(c["theme"])}" aria-pressed="false" hidden>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.7 14.2A8.9 8.9 0 0 1 9.8 3.3a9 9 0 1 0 10.9 10.9Z"/></svg>
        </button>
      </div>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer">
    <div class="shell footer-inner">
      <a class="wordmark" href="{home}">{wordmark()}</a>
      <div class="footer-links"><a href="{route(lang, "privacy")}">{esc(c["privacy"])}</a>
      <a href="{route(lang, "terms")}">{esc(c["terms"])}</a></div>
      <small>© {esc(BRAND)}</small>
    </div>
  </footer>
</body>
</html>
'''


def homepage(lang, apps):
    c = COPY[lang]
    cards = []
    for field, detail, icon in zip(FIELDS, c["business"], ICONS):
        cards.append(f'''<article class="card">
          <div class="card-icon"><svg viewBox="0 0 24 24" aria-hidden="true">{icon}</svg></div>
          <h3 lang="en">{esc(field)}</h3><p>{esc(detail)}</p>
        </article>''')
    org = json.dumps({
        "@context": "https://schema.org", "@type": "Organization",
        "name": BRAND, "alternateName": "센텀노바", "url": SITE + "/",
        "email": EMAIL, "address": c["address"],
    }, ensure_ascii=False).replace("<", "\\u003c")
    return layout(lang, "home", BRAND, f'''
    <section class="hero" aria-labelledby="hero-title">
      <div class="shell hero-inner">
        <div class="hero-copy">
          <div class="hero-brand"><span aria-hidden="true"></span>{esc(BRAND)}</div>
          <h1 id="hero-title">{multiline(c["slogan"])}</h1>
          <p>{multiline(c["intro"])}</p>
          <div class="hero-actions">
            <a class="button primary" href="#business">{esc(c["nav"][2])} <span aria-hidden="true">↓</span></a>
            <a class="button outline" href="#contact">{esc(c["nav"][4])} {ARROW}</a>
          </div>
        </div>
        <div class="art" aria-hidden="true"><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div>
          <div class="orbit orbit-c"></div><div class="planet"></div><div class="satellite"></div><div class="spark"></div>
        </div>
      </div>
    </section>
    <section class="section shell about" id="about" aria-labelledby="about-title">
      <div><p class="section-label">{esc(c["nav"][1])}</p><h2 id="about-title">{multiline(c["about_title"])}</h2></div>
      <div class="about-copy">{"".join(f"<p>{esc(p)}</p>" for p in c["about"])}</div>
    </section>
    <section class="section services" id="business" aria-labelledby="business-title">
      <div class="shell"><p class="section-label">{esc(c["nav"][2])}</p><h2 id="business-title">{esc(c["business_title"])}</h2>
      <p class="section-intro">{esc(c["business_intro"])}</p><div class="card-grid">{"".join(cards)}</div></div>
    </section>
    <section class="section shell apps" id="apps" aria-labelledby="apps-title">
      <p class="section-label">{esc(c["nav"][3])}</p><h2 id="apps-title">{esc(c["apps_title"])}</h2>
      {app_cards(apps, lang)}
    </section>
    <section class="section contact" id="contact" aria-labelledby="contact-title">
      <div class="shell contact-inner">
        <div><p class="section-label">{esc(c["nav"][4])}</p><h2 id="contact-title">{esc(c["contact_title"])}</h2>
        <p>{esc(c["contact_intro"])}</p><a class="button primary" href="mailto:{EMAIL}">{esc(c["contact_action"])} {ARROW}</a></div>
        <address><strong>{esc(c["name"])}</strong><span>{esc(c["representative"])}</span>
        <span>{esc(c["address"])}</span><a href="mailto:{EMAIL}">{EMAIL}</a></address>
      </div>
    </section>
    <script type="application/ld+json">{org}</script>''')


def document(lang, page):
    c = COPY[lang]
    sections = []
    for heading, paragraph in c[f"{page}_sections"]:
        sections.append(f"<section><h2>{esc(heading)}</h2><p>{esc(paragraph)}</p></section>")
    links = f'<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>'
    if page == "privacy":
        label = "GitHub 개인정보처리방침" if lang == "ko" else "GitHub Privacy Statement"
        links += f'<p><a href="{GITHUB_PRIVACY}">{label} {ARROW}</a></p>'
    return layout(lang, page, c[page], f'''
    <article class="shell document"><h1>{esc(c[page])}</h1>{"".join(sections)}{links}</article>''')


def build(publish=False):
    apps = json.loads((ROOT / "data/apps.json").read_text(encoding="utf-8"))
    if not isinstance(apps, list):
        raise ValueError("data/apps.json must contain an array.")
    files = {}
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for lang in LANGUAGES:
        c = COPY[lang]
        for page in PAGES:
            url = route(lang, page)
            path = url.lstrip("/") + ("index.html" if url.endswith("/") else "")
            if page == "404":
                files[path] = layout(lang, page, c["missing"], f'''
                <section class="shell document missing"><h1>{esc(c["missing"])}</h1>
                <p>{esc(c["missing_body"])}</p><a class="button primary" href="{route(lang)}">{esc(c["nav"][0])}</a></section>''')
                continue
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = SITE + url
            files[path] = homepage(lang, apps) if page == "home" else document(lang, page)

    output = ROOT / "_site"
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(ROOT / "public", output)
    shutil.copytree(ROOT / "assets", output / "assets")
    for path, content in files.items():
        destination = output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    ET.ElementTree(sitemap).write(output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (output / ".nojekyll").touch()
    if publish:
        for source in output.rglob("*"):
            if source.is_file() and source.name != ".nojekyll":
                destination = ROOT / source.relative_to(output)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists() or destination.read_bytes() != source.read_bytes():
                    shutil.copyfile(source, destination)
    print(f"Built {len(files)} pages in {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Update the main-branch Pages files.")
    build(publish=parser.parse_args().publish)
