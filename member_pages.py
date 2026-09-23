"""Static roster and individual pages; replace provisional records in data/members.json."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def e(value):
    return escape(str(value), quote=True)

def make_member_pages():
    records = json.loads((ROOT / 'data/members.json').read_text())
    players = sorted((r for r in records if r['kind'] == 'player'),
                     key=lambda r: (r['number'] is None, int(r['number']) if r['number'] is not None else r['preview_number']))
    staff = [r for r in records if r['kind'] == 'staff']
    ordered = players + staff
    assert len({r['id'] for r in ordered}) == len(ordered), 'Duplicate member ID'

    def label(r):
        if r['kind'] == 'staff':
            return r['role']
        return str(r['number']) if r['number'] is not None else f"{r['preview_number']:02}"

    def photo(r):
        return f'''<div class="member-visual {'is-placeholder' if r['placeholder'] else ''} {'is-portrait' if r.get('image_layout') == 'portrait' else ''}">
          <span class="member-watermark" aria-hidden="true">{e(label(r))}</span>
          <img class="member-image" src="{e(r['image'])}" alt="{'個人写真準備中の仮アバター' if r['placeholder'] else e(r['name'])}" width="150" height="150" loading="lazy">
          {'<span class="photo-pending">PHOTO COMING SOON</span>' if r['placeholder'] else ''}</div>'''

    def card(r):
        return f'''<a class="member-card" href="member-{e(r['id'])}.html">
          {photo(r)}<div class="member-card-info"><span class="member-number">{e(label(r))}<small>{'仮番号' if r['kind']=='player' and r['number'] is None else ''}</small></span>
          <div><span class="member-role">{e(r['position'] or ('POSITION —' if r['kind']=='player' else 'COACHING STAFF'))}</span><h3>{e(r['name'])}</h3><span class="member-english">{e(r['english_name'] or 'NAME TO BE ANNOUNCED')}</span></div><span class="member-arrow" aria-hidden="true">↗</span></div></a>'''

    notice = 'レイアウト確認用：氏名・背番号・プロフィールは仮表示です。個人写真が未準備の枠には仮アバター・エンブレムを使用しています。'
    listing = f'''<section class="roster-heading"><div class="wrap"><div class="breadcrumb"><a href="index.html">ホーム</a> / メンバー紹介</div><div class="eyebrow">THE PEOPLE OF CASTINIO</div><h1>MEMBERS<span>メンバー紹介</span></h1><p>この仲間と、楽しく、真剣に。</p><nav class="roster-jumps" aria-label="メンバー区分"><a href="#players">選手 <b>{len(players):02}</b></a><a href="#staff">監督・コーチ <b>{len(staff):02}</b></a></nav></div></section>
    <div class="wrap"><p class="roster-notice">{notice}</p></div>
    <section class="section roster-section" id="players"><div class="wrap"><div class="roster-section-title"><div><div class="eyebrow">PLAYERS</div><h2>選手</h2></div><p>背番号順 <span>／ {len(players)} PLAYERS</span></p></div><div class="member-grid">{''.join(card(r) for r in players)}</div></div></section>
    <section class="section pale" id="staff"><div class="wrap"><div class="roster-section-title"><div><div class="eyebrow">COACHING STAFF</div><h2>監督・コーチ</h2></div></div><div class="member-grid">{''.join(card(r) for r in staff)}</div></div></section>'''
    comparison = '''<aside class="motion-comparison" aria-label="動きの比較"><div class="wrap motion-controls"><span>動きの比較</span><div role="group" aria-label="アニメーションの種類"><button type="button" data-motion="adopted" aria-pressed="true">採用版：元の動き＋光</button><button type="button" data-motion="original" aria-pressed="false">A：今の動き</button><button type="button" data-motion="bold" aria-pressed="false">B：大胆な動き</button></div><button type="button" id="motion-play">動きを再生</button><span id="motion-status" role="status">A：今の動き</span></div></aside>'''
    listing = comparison + listing + '<script src="members-motion.js" defer></script>'
    pages = {'members': ('メンバー紹介｜FCカスティーニオ', listing)}
    for i, r in enumerate(ordered):
        fields = [('氏名', r['name']), ('英語表記', r['english_name'] or '準備中')]
        if r['kind'] == 'player':
            fields += [('背番号', str(r['number']) if r['number'] is not None else label(r)+'（レイアウト確認用の仮番号）'), ('ポジション', r['position'] or '準備中')]
        else:
            fields += [('役職', r['role'])]
        fields += [('サッカー歴', r['history'] or '準備中')]
        adjacent = ''
        if i > 0:
            adjacent += f'<a href="member-{e(ordered[i-1]["id"])}.html">← 前のメンバー</a>'
        adjacent += '<a href="members.html#'+('players' if r['kind']=='player' else 'staff')+'">一覧に戻る</a>'
        if i+1 < len(ordered):
            adjacent += f'<a href="member-{e(ordered[i+1]["id"])}.html">次のメンバー →</a>'
        body = f'''<section class="profile-heading"><div class="wrap"><div class="breadcrumb"><a href="index.html">ホーム</a> / <a href="members.html">メンバー紹介</a> / {e(r['name'])}</div><p class="roster-notice">{notice}</p><div class="profile-layout"><div class="profile-image">{photo(r)}</div><div class="profile-intro"><div class="eyebrow">{'PLAYER PROFILE' if r['kind']=='player' else 'STAFF PROFILE'}</div><div class="profile-number">{e(label(r))}<small>{'仮番号' if r['kind']=='player' and r['number'] is None else ''}</small></div><h1>{e(r['name'])}</h1><p class="member-english">{e(r['english_name'] or 'NAME TO BE ANNOUNCED')}</p><p>{e(r['position'] or (r.get('role') or 'ポジション準備中'))}</p></div></div></div></section>
        <section class="section"><div class="wrap narrow"><div class="eyebrow">PROFILE</div><h2>プロフィール</h2><dl class="profile-facts">{''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in fields)}</dl><div class="profile-message"><div class="eyebrow">MESSAGE</div><h2>ひとこと</h2><p>{e(r['message'] or '紹介メッセージは準備中です。')}</p></div><nav class="profile-pagination" aria-label="メンバーページの移動">{adjacent}</nav></div></section>'''
        pages['member-'+r['id']] = (r['name']+'｜FCカスティーニオ', body)
    return pages
