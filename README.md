# Paper_Error_Checker

## Overview
論文の文法ミスや凡ミスのチェックを自動的に行うツールです。
このツールの利点は以下です。
- 機械的なチェックを自動化することで、論文執筆の労力を削減・チェック漏れを無くす
- 安積先生・査読者・英文校正などに指摘された凡ミスや文法ミスを容易に共有でき、チェックする人が同じミスを指摘しなくて良い・チェックが厳しくなることで全員の論文のクオリティが上がる

コマンドの実行結果の例は以下です

![スクリーンショット 2022-06-08 160901](https://user-images.githubusercontent.com/55824710/172570896-c274ab77-fbb5-44f1-9b80-e4404c813cfb.png)


## Setup Flow
```
git clone https://github.com/atsushi421/Paper_Error_Checker.git
cd Paper_Error_Checker
./setup.bash
```

## Run
`bash run_checker.bash -d [PATH]`
- [PATH]: チェック対象の .tex ファイルを全て含んだディレクトリへのパス

## How to add a check
`Paper_Error_Checker/src/check_lists/check_list.yaml` に追記することで、簡単にチェック項目を追加できます。
チェック項目の記述方法は以下です。
```
message:
  pattern: [RAW_STRING]
  level: "error", "warning" or "info"
  target: "all", "introduction", or "abstract"
  flags: "ignorecase" (optional)
```
- [RAW_STRING] : 検出したい正規表現のパターン
    - (例): 'a 母音で始まる単語の冠詞' を検出したい場合 ->
    `'(?:^a|\sa) (?:[aiueo]|{\\it [aiueo]'`
- level: 警告のレベル
    - "error": 絶対に直すべきミス
    - "warning": we の使用など、極力減らすべきこと
    - "info": 英文校正で指摘されるような英語表現の修正
- target: チェックの範囲
    - "all": 対象ディレクトリ内の全ての .tex ファイルをチェック
    - "introduction": intro がファイル名に入っている .tex ファイルのみをチェック
    - "abstract": abst がファイル名に入っている .tex ファイルのみをチェック
- flags: 正規表現のマッチ判定に使用されるオプション
    - "ignorecase": 大文字・小文字を区別しない
