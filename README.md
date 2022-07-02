# PaperErrorChecker

## Overview
論文の凡ミスチェックを自動的に行うツールです。
このツールの利点は以下です。
- 機械的なチェックを自動化することで、論文執筆の労力を削減・チェック漏れを無くす
- 安積先生・査読者・英文校正などに指摘された凡ミスや文法ミスを容易に共有でき、チェックする人が同じミスを指摘しなくて良い・チェックが厳しくなることで全員の論文のクオリティが上がる

コマンドの実行結果の例は以下です

![スクリーンショット 2022-06-09 085657](https://user-images.githubusercontent.com/55824710/172736685-6d2cd208-fb8f-48d2-bf45-471a820f2c39.png)

なお、英文法ミスのチェックは他にも優れたツールが公開されているため、本ツールは、論文(tex)特有の書き方や、安積研特有の書き方等をチェックするのが主なユースケースです。


## Setup Flow
```
git clone https://github.com/atsushi421/PaperErrorChecker.git
cd PaperErrorChecker
./setup.bash
```

## Usage
`./run_checker.bash -d [PATH] -f [FORMAT]`
- [PATH]: チェック対象の .tex ファイルを全て含んだディレクトリへのパス
- [FORMAT]：投稿先に合わせてチェックリストを切り替える。現在サポートしているのは以下
    - conference: 国際学会
    - thesis: 修論・卒論

## How to add a check
`PaperErrorChecker/src/check_lists/` 下の .yaml ファイルに追記することで、簡単にチェック項目を追加できます。
各ファイルの対応は以下です。
- `common.yaml`: フォーマットに依存しないチェック項目
- `conference.yaml`: 国際学会に投稿する論文のチェック項目
- `thesis.yaml`: 卒論・修論のチェック項目

チェック項目の記述方法は以下です。
```
message:
  pattern: [RAW_STRING]
  level: "error", "warning" or "info"
  target: "all", "introduction", or "abstract"
  flags: "ignorecase" (optional)
```
- message: ユーザに表示したい警告メッセージや、具体的な修正方法
    - (例) \cite{X}, \cite{Y} -> \cite{X, Y}
- [RAW_STRING] : 検出したい正規表現のパターン
    - (例): 上の例を検出したい場合 -> `'\\cite{\w+}[, ]*\\cite'`
- level: 警告のレベル
    - "error": 絶対に直すべきミス
    - "warning": we の使用など、極力減らすべきこと
    - "info": 英文校正で指摘されるような英語表現の修正など
- target: チェックの範囲
    - "all": 対象ディレクトリ内の全ての .tex ファイルをチェック (default)
    - "introduction": intro がファイル名に入っている .tex ファイルのみをチェック
    - "abstract": abst がファイル名に入っている .tex ファイルのみをチェック
- flags: 正規表現のマッチ判定に使用されるオプション
    - "ignorecase": 大文字・小文字を区別しない

### Flow for adding checks
チェック項目を追加する際の理想のフローです。ただ、追加するハードルは低くしたいので、slack や issue で「こういうチェックをしたい」と伝えてもらうだけでも大丈夫です。
1. [PaperErrorChecker](https://github.com/azu-lab/PaperErrorChecker) リポジトリをフォーク
2. `PaperErrorChecker/src/check_lists/` 下の .yaml ファイルにチェック項目を追加
3. (出来る限り) `PaperErrorChecker/tests/check_lists/` 下にテストコードを書く
4. Push し、azu-lab/PaperErrorChecker の dev ブランチに PR を出す
    - reviewer に atsushi421 を追加してください
    - PR 出した際に、github action の pytest でエラーが出ていない事を確認してください
5. 問題なければマージします

## Note
`target: "introduction"` や `"abstract"` を使用したい場合は、イントロやアブストを別ファイルとして分けてください（e.g., Introduction.tex or Abstract.tex）。

このツールのチェックの精度は正規表現のパターンに依存しており、現在は Atsushi がスピード重視で書いたものなので、誤検出が多数あります。
ただし、パターンを完璧にするのは難易度が高く、時間がかかるので、多少誤検出があったとしても、ユーザが判断すれば良いかなと考えています。

### TODO
実装出来ていませんが、欲しい機能・やりたいことです。全員で協力すれば良い物が出来ると思うので、issue, PR 大歓迎です。
- 誤検出を無くす
- 全てのチェック項目のテストコードを書く
- [IPSJ, APRIS フォーマット](https://docs.google.com/spreadsheets/d/1CSIPXggHC_4Hg4Thrny_9vVVM13q9O2u/edit#gid=1600829807) のチェックリストを作り、IPSJ_APRIS オプションを追加する
- [日本語原稿](https://docs.google.com/spreadsheets/d/1CSIPXggHC_4Hg4Thrny_9vVVM13q9O2u/edit#gid=709246267) に対応
- チェック項目を増やす

### Development ideas
機能拡張のアイデアです。あったら良いな程度です。
- 誤検出を無くし、自動で置換できるようにする
- [spaCy](https://spacy.io/api) などの自然言語処理ライブラリを絡めれば、時制・3単現のチェックとかもできそう
