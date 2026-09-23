"""Assemble local HTML previews using only Python's standard library."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'dist'
PAGES = {
    'index': ('ホーム', 'FCカスティーニオ｜神戸の社会人サッカーチーム'),
    'team': ('チーム紹介', 'チーム紹介｜FCカスティーニオ'),
    'activities': ('活動紹介', '活動紹介｜FCカスティーニオ'),
    'join': ('選手募集', '選手募集｜FCカスティーニオ'),
    'match': ('対戦相手募集', '対戦相手募集｜FCカスティーニオ'),
    'contact': ('お問い合わせ', 'お問い合わせ｜FCカスティーニオ'),
}
BRAND = '''<img src="assets/emblem-instagram.jpg" width="54" height="54" alt="">
      <span>
        <strong>FC CASTINIO</strong>
        <small>FCカスティーニオ</small>
      </span>'''

for slug, (label, title) in PAGES.items():
    source = ROOT / 'pages' / f'{slug}.html'
    if not source.exists():
        continue
    links = []
    for key, (text, _) in PAGES.items():
        if key == 'index':
            continue
        current = ' aria-current="page"' if key == slug else ''
        cls = ' class="nav-contact"' if key == 'contact' else ''
        links.append(f'        <a href="{key}.html"{current}{cls}>{text}</a>')
    nav_links = '\n'.join(links)
    document = f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>{escape(title)}</title>
  <meta name="description" content="神戸市リーグに所属する社会人サッカーチーム、FCカスティーニオ。楽しく真剣に、仲間とのコミュニケーションを大切に活動しています。">
  <link rel="icon" type="image/jpeg" href="assets/emblem-instagram.jpg">
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">本文へスキップ</a>

  <div class="topline">
    <div class="wrap">
      <span>KOBE CITY FOOTBALL LEAGUE</span>
      <span>神戸市を拠点に活動する社会人サッカーチーム</span>
    </div>
  </div>

  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="FCカスティーニオ ホーム">{BRAND}</a>
      <button class="menu-button" type="button" aria-expanded="false" aria-controls="navigation">メニュー</button>
      <nav class="nav" id="navigation" aria-label="メインメニュー">
{nav_links}
      </nav>
    </div>
  </header>

  <main id="main">{source.read_text()}</main>

  <footer class="footer">
    <div class="wrap">
      <div class="footer-top">
        <a class="brand" href="index.html" aria-label="FCカスティーニオ ホーム">{BRAND}</a>
        <div class="footer-links">
          <a href="team.html">チーム紹介</a>
          <a href="contact.html">お問い合わせ</a>
          <a href="https://www.instagram.com/fc.castinio/" target="_blank" rel="noopener noreferrer">Instagram ↗</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span>神戸市内 · 土日を中心に週1回程度活動</span>
        <span>© FC CASTINIO</span>
      </div>
    </div>
  </footer>
</body>
</html>'''
    (DEST / f'{slug}.html').write_text(document)
    print(f'Generated {slug}.html')
