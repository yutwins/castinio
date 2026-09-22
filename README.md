# FCカスティーニオ HTMLプレビュー

WordPress制作の前に画面・導線を確認する静的HTMLの試作。Cloudflare Pagesで公開中。お問い合わせフォームはCloudflare Pages Functions経由で実際に送信される。管理画面・記事投稿は未実装。

## フォルダ構成

```text
site/
├── README.md
├── build_preview.py       共通ヘッダー・フッターとページを組み立てる
├── pages/                 ページ本文（編集元）
│   ├── index.html
│   ├── team.html
│   ├── activities.html
│   ├── join.html
│   ├── match.html
│   └── contact.html
├── dist/                  ブラウザ確認用・公開用。HTMLを直接開くことも可能
│   ├── *.html             組み立て後のページ
│   ├── styles.css         共通スタイル（直接編集する）
│   ├── app.js             メニュー・お問い合わせフォーム送信
│   └── assets/            この試作で使用する素材のコピー
└── functions/api/contact.js  お問い合わせフォームを受け付けるCloudflare Pages Function
```

CSS/JSと素材はdist内のファイルが編集元。HTMLはpagesまたはbuild_preview.pyを編集して再生成する。Pythonの標準機能だけで動作し、外部パッケージは不要。

## 再生成とプレビュー

プロジェクトの football-club-website/ で実行する。

```sh
python3 site/build_preview.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory site/dist
```

ブラウザで http://127.0.0.1:8765/ を開く。ローカルサーバー停止後は再起動するか、dist/index.htmlを直接開く。外部公開用サーバーとしては使用しない。

## 試作の範囲と制約

- 青を基調、赤をアクセントとし、提供写真5枚と公式Instagramのエンブレムを使用。
- 6ページ、モバイルメニュー、募集からフォームへの種別引き継ぎを実装。
- お問い合わせフォームは入力検証後、Cloudflare Turnstileで確認のうえ /api/contact に送信し、Cloudflare KVに保存する。JavaScript無効時は送信しない。
- すべてのページにnoindex,nofollowを設定。
- 未確認の日付やスコアは掲載しない。活動紹介は概要ページで、記事一覧・記事詳細・最新記事の自動反映はWordPress化する段階で作る。
- 写真は元画像のコピー。公開前に画像容量・位置情報等のメタデータを処理する。エンブレムは150pxで、大きな表示には不向き。
- 独自ドメインは未契約（*.pages.devで公開中）。

## お問い合わせフォームの設定（Cloudflare側で1回だけ必要）

`functions/api/contact.js` はTurnstileでの検証とKVへの保存を行う。以下をCloudflareダッシュボードで設定する。

1. **KV namespace**: Workers & Pages → KV でnamespaceを作成し、Pagesプロジェクトの設定（Settings → Functions → KV namespace bindings）で変数名 `CONTACT_SUBMISSIONS` として紐付ける。
2. **Turnstile**: Site keyは設定済み（`pages/contact.html` の `data-sitekey`）。Secret keyはPagesプロジェクトの環境変数（Settings → Environment variables）に `TURNSTILE_SECRET_KEY` として登録する（Secret扱い）。
3. 保存された問い合わせ内容はCloudflareダッシュボードのKV namespaceから確認する。通知メールは送られないため、定期的に確認する運用が必要。

## 確認済み

- 全6ページを390pxと1440px幅で表示し、横はみ出しがないことを確認。
- トップのPC・スマートフォン表示を目視確認。モバイルメニューの開閉と遷移を確認。
- 選手募集からフォームへ移動すると種別が選択されることを確認。
- 未入力で確認できないこと、有効な入力後に未送信の案内が表示されることを確認。
- 全HTMLのローカルリンク・画像・スクリプト・ページ内アンカーの参照先を検証。
