# 参照資料 出典一覧

本ディレクトリに格納されている参照ファイルおよび関連参照文書の出典を記載する。

---

## summitslist.csv

| 項目 | 内容 |
|---|---|
| タイトル | SOTA山岳リスト |
| 提供元 | [SOTA Database](https://www.sotadata.org.uk/) |
| 取得元URL | <https://www.sotadata.org.uk/summitslist.csv> |
| 配置場所 | `$DATA_DIR/ref/summitslist.csv`（git 管理外・ユーザー手動配置） |
| 備考 | JAで始まるサミットが日本支部対象。定期的に更新されるため再取得時は日付を確認すること。 |

---

## SOTA-Summit-list-revision-request.xlsx

| 項目 | 内容 |
|---|---|
| タイトル | SOTA日本支部 山岳データ登録変更申請書 |
| 提供元 | [SOTA日本山岳リスト](https://www.kawauchi.homeip.mydns.jp/sotajp/) |
| 取得元URL | <https://www.kawauchi.homeip.mydns.jp/sotajp/wp-content/uploads/2024/03/SOTA-Summit-list-revision-request.xlsx> |
| 備考 | 申請書テンプレート。1シート構成。アクション列に追加・変更・削除・その他を選択して申請する。 |

---

## geojson_v{N}/（バージョン番号付きディレクトリ）

配置場所: `$DATA_DIR/ref/geojson_v{N}/`（git 管理外・ユーザー手動配置）。ディレクトリ名はダウンロード時のバージョン番号を含む（例: `geojson_v31/`）。
更新時は新バージョンのディレクトリを追加し、古いバージョンは削除して運用する。

| 項目 | 内容 |
|---|---|
| タイトル | SOTA日本山名リスト GeoJSON |
| 提供元 | [ジオサミットでひとこえ](https://little-ctc.com/sota_hp/geojson/) |
| 取得元URL | <https://little-ctc.com/?sdm_process_download=1&download_id=11249> |
| ファイル構成 | ja0〜ja9（エリア別10ファイル）。ja0=全国、ja1〜ja9=各地方ブロック。 |
| 備考 | 国土地理院地図での目視確認・申請内容のエビデンス用途で参照する。 |

---

## 国土地理院標高タイル（データソース）

| 項目 | 内容 |
|---|---|
| 提供元 | 国土地理院 |
| データ種別 | DEM5a / DEM5b / DEM5c（ズームレベル 15）、DEM10b（ズームレベル 14）、DEM1a（ズームレベル 17。HTML ビューアの等高線だけ） |
| 参照 URL | <https://maps.gsi.go.jp/development/ichiran.html> |
| 利用規約 | 国土地理院コンテンツ利用規約（https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html） |
| 帰属表示義務 | 利用成果物に「国土地理院」の帰属表示が必要 |
| 本プロジェクトでの利用形態 | タイルをローカルキャッシュとして保存して標高解析に使用。タイルデータ自体はリポジトリに含めない（.gitignore）。生成する HTML ビューアの帰属表示に `© 国土地理院` を含める。HTML ビューアの等高線オーバーレイは、表示範囲の DEM1a・DEM5a〜5c・DEM10b をブラウザから実行時取得する（[ADR-SRS-015](../docs/decisions/ADR-SRS-015-contour-overlay.md)・[ADR-SRS-067](../docs/decisions/ADR-SRS-067-contour-uses-dem1a-at-high-zoom.md)）。 |

---

## 国土地理院 地図タイル（標準地図・淡色地図）

| 項目 | 内容 |
|---|---|
| 提供元 | 国土地理院 |
| データ種別 | 標準地図（`std`）・淡色地図（`pale`）。ラスタタイル（PNG） |
| 取得 URL | 標準地図: `https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png`<br>淡色地図: `https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png` |
| 参照 URL | <https://maps.gsi.go.jp/development/ichiran.html> |
| 利用規約 | 国土地理院コンテンツ利用規約（https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html） |
| 帰属表示義務 | 利用成果物に「国土地理院」の帰属表示が必要 |
| 本プロジェクトでの利用形態 | HTML ビューアの背景地図タイルとして使用（OSM・OpenTopoMap との切り替え用）。表示範囲のタイルをブラウザから実行時取得して描画する。タイルデータはリポジトリに含めない。ビューアの帰属表示に `© 国土地理院` を含める。選定経緯: [ADR-SRS-006](../docs/decisions/ADR-SRS-006-viewer-background-tile-selection.md) |

---

## OpenStreetMap（地図タイル）

| 項目 | 内容 |
|---|---|
| 提供元 | OpenStreetMap contributors |
| 利用規約 | Open Database License (ODbL) — <https://www.openstreetmap.org/copyright> |
| 帰属表示義務 | 利用成果物に `© OpenStreetMap contributors` の表示が必要 |
| 本プロジェクトでの利用形態 | HTML ビューアの背景地図タイルとして使用（国土地理院地図・OpenTopoMap との切り替え用） |

---

## OpenTopoMap（地図タイル）

| 項目 | 内容 |
|---|---|
| 提供元 | OpenTopoMap contributors |
| 利用規約 | CC-BY-SA — <https://opentopomap.org/about#verwendung> |
| データソース | OpenStreetMap データ（ODbL）+ SRTM 標高データ |
| 帰属表示義務 | 利用成果物に `© OpenTopoMap contributors` の表示が必要 |
| 本プロジェクトでの利用形態 | HTML ビューアの背景地図タイルとして使用（等高線・山名確認用） |

---

## 国土地理院 基準点タイル（データソース）

| 項目 | 内容 |
|---|---|
| 提供元 | 国土地理院 |
| データ種別 | 基準点（電子基準点・一等／二等／三等三角点）。ベクトルタイル（GeoJSON 形式） |
| 取得 URL | `https://cyberjapandata.gsi.go.jp/xyz/cp/{z}/{x}/{y}.geojson` |
| 参照 URL | <https://maps.gsi.go.jp/development/ichiran.html> |
| 利用規約 | 国土地理院コンテンツ利用規約（https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html） |
| 帰属表示義務 | 利用成果物に「国土地理院」の帰属表示が必要 |
| 本プロジェクトでの利用形態 | HTML ビューアの「基準点」参照レイヤー（デフォルト OFF）で、表示範囲のタイルをブラウザから実行時取得して描画する。タイルデータはリポジトリに含めない。レイヤー ON 時にビューアの帰属表示へ基準点データの出典として `国土地理院` を併記する。採用経緯: [ADR-SRS-034](../docs/decisions/ADR-SRS-034-viewer-reference-layers.md) |

---

## 参照文書（ファイル未格納）

### SOTA日本支部 参照マニュアル（標高バンド・ポイント算出ルール）

| 項目 | 内容 |
|---|---|
| タイトル | SOTA日本支部 参照マニュアル 2025年7月改定版 |
| 提供元 | [SOTA日本支部](https://www.kawauchi.homeip.mydns.jp/sotajp/) |
| 参照URL | <https://www.kawauchi.homeip.mydns.jp/sotajp/%e3%82%84%e3%81%a3%e3%81%a6%e3%81%bf%e3%82%88%e3%81%86/> （セクション「8. その場所は何ポイント?」） |
| 備考 | 標高バンドに基づくポイント数（1/2/4/6/8/10）の算出表を規定。全国統一（地域依存なし）。本プロジェクトでは `points` / `sota_points` の算出根拠として参照する。詳細な表は `docs/00_GLOSSARY.md` の「標高バンド（Points 算出表）」を参照。 |

---

### SOTA日本支部 FAQ

| 項目 | 内容 |
|---|---|
| タイトル | SOTA日本支部 よくある質問（FAQ） |
| 提供元 | [SOTA日本支部](https://www.kawauchi.homeip.mydns.jp/sotajp/) |
| URL | <https://www.kawauchi.homeip.mydns.jp/sotajp/faqs/> |
| 備考 | アクティベーションゾーンの定義（Q12: 「山頂の最高地点で運用することは...このような時のために、山頂の高度から25m以内の高度差であれば山頂からの運用とみなします。この25mの高度差のエリアをアクティベーションゾーンとしています。」）等、SOTAルールの参照に使用。 |

---

### 国土数値情報 N03 行政区域

| 項目 | 内容 |
|---|---|
| タイトル | 国土数値情報 行政区域データ（N03-2026） |
| 提供元 | [国土交通省 国土数値情報ダウンロードサービス](https://nlftp.mlit.go.jp/) |
| URL | <https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2026.html> |
| ファイル形式 | ZIP（`N03-YYYYMMDD_GML.zip`、全国版・約766MB）。GML・Shapefile・GeoJSON を同梱、うち市区町村単位 GeoJSON は約580MB |
| 主要属性 | `N03_001`=都道府県名、`N03_002`=北海道振興局名、`N03_007`=行政区域コード（北方領土除外 01695〜01700 の判定に使用） |
| 利用規約 | 国土数値情報利用規約（https://nlftp.mlit.go.jp/ksj/other/agreement.html） |
| 本プロジェクトでの利用形態 | [FR-017](../docs/20_SRS.md#fr-017-n03-行政区域前処理データ準備)（N03 行政区域前処理）の入力。`$DATA_DIR/ref/` 直下に配置し、前処理で N03 前処理済み地域 GeoJSON（60地域）・市区町村 GeoJSON・北方領土除外タイルリストを生成する。ファイルサイズが大きいため git 管理外（.gitignore）。 |

---

### 日本の国土にかかる第1次地域区画

| 項目 | 内容 |
|---|---|
| タイトル | 日本の国土にかかる第1次地域区画（メッシュコード定義） |
| 提供元 | [政府統計の総合窓口（e-Stat）](https://www.e-stat.go.jp/) |
| 整備 | 総務省統計局 |
| 運用管理 | 独立行政法人統計センター |
| 参照URL | <https://www.e-stat.go.jp/pdf/gis/primary_mesh_jouhou.pdf> |
| 備考 | 解析に使用する1次メッシュコード（4桁）の地理的範囲の定義元。HTML ビューアの 1 次メッシュのグリッドは、この一覧の 176 件（竹島を含む 5531 を含む）を描く。解析の一覧は 5531 を除く（[ADR-URD-009](../docs/decisions/ADR-URD-009-takeshima-exclusion.md)）。 |

---

### 開発プロセスの参照規格

開発文書とプロセスが参照する規格の目録。どれを何に使うか、「参照」と「準拠」の違い、意図して保つ形は [ADR-OPS-002](../docs/decisions/ADR-OPS-002-reference-standards-and-intended-deviations.md) が正本。規格の版の正本も ADR-OPS-002 の表で、下の表に記載する版は、その写しである。規格の本文は持っていない。

| 規格 | 題 | 目録 |
|---|---|---|
| ISO/IEC/IEEE 12207:2026 | Systems and software engineering — Software life cycle processes | <https://www.iso.org/standard/90219.html> |
| ISO/IEC/IEEE 29148:2018 | Systems and software engineering — Life cycle processes — Requirements engineering | <https://www.iso.org/standard/72089.html> |
| ISO/IEC/IEEE 42010:2022 | Software, systems and enterprise — Architecture description | <https://www.iso.org/standard/74393.html> |
| ISO/IEC/IEEE 29119-1:2022 | Software and systems engineering — Software testing — Part 1: General concepts | <https://www.iso.org/standard/81291.html> |
| ISO/IEC/IEEE 29119-2:2021 | Software and systems engineering — Software testing — Part 2: Test processes | <https://www.iso.org/standard/79428.html> |
| ISO/IEC/IEEE 29119-3:2021 | Software and systems engineering — Software testing — Part 3: Test documentation | <https://www.iso.org/standard/79429.html> |
| ISO/IEC 25010:2023 | Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model | <https://www.iso.org/standard/78176.html> |
| ISO/IEC/IEEE 24765:2017 | Systems and software engineering — Vocabulary | <https://www.iso.org/standard/71952.html>（オンライン版の SEVOCAB: <https://www.computer.org/sevocab>） |
| ISTQB CTFL シラバス v4.0.1 | Certified Tester Foundation Level Syllabus v4.0.1 | <https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf> |
| ISTQB 用語集 | ISTQB Glossary（オンライン版、版を固定しない） | <https://glossary.istqb.org/> |
| 二次資料: 29148:2018 に基づくとする SRS の雛形 | ISO/IEC/IEEE 29148:2018 Software Requirements Specification（第三者の公開の雛形。規格の本文ではない） | <https://github.com/G7DAO/idea-submission-guidelines/blob/main/SRS-Template.md> |
| 二次資料: 25010:2023 の特性と副特性の一覧 | arc42 Quality Model の「ISO/IEC 25010 - Systems and Software Quality」と「Update on ISO 25010, version 2023」（第三者の解説。規格の本文ではない） | <https://github.com/arc42/quality.arc42.org-site>（commit `713c46f8fb98`、2026-10-05 の時点。`_standards/iso/iso-25010.md`、`_articles/07-iso-25010-update-2023.md`、`images/articles/iso-25010/ISO-25010-2023-detailed.png`） |

- 確認日: 2026-10-07。ISO の目録ページの題・版・状態を、Web 検索の結果に出た目録ページで確かめた（作業環境から iso.org へ直接は接続できなかった）。
- 改訂の動き（2026-10-07 時点）: 12207:2026 は 12207:2017 を置き換えた。29148 は次の版の委員会原案が、24765 は第 3 版の国際規格案（DIS）が進行中。
- 25010:2023 の特性と副特性は、2026-10-08 に上の arc42 のソースを取得して確かめた。ソースの表は Testability を Flexibility の行に置くが、同じリポジトリの詳細図は Maintainability の下に置くので、図に従う。iso.org には作業環境から接続できず、規格の本文と ISO の公式の見本は読んでいない。
- CTFL シラバス v4.0.1 は、2026-10-08 に上の URL から PDF を取得し、2.2（2.2.1 を含む）・5.1.1・5.1.3 の原文を読んだ（取得した PDF の SHA-256 は `3b072f81db5c7671aadacc42553e726faa93913a969cc7a89e9dc28c2318d1f1`）。
