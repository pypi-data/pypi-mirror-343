# LynxKit-Markdown

指定されたURLからWebページのコンテンツを取得し、Markdown形式に変換するシンプルなPythonツールです。

内部で `markitdown` ライブラリを利用し、一時ファイルを経由してHTMLからMarkdownへの変換を行っています。

## 概要

このツールは、Webページの内容を素早くMarkdown形式で取得したい場合に役立ちます。主な処理の流れは以下の通りです。

1.  指定されたURLにアクセスし、HTMLコンテンツを取得します。
2.  取得したHTMLを一時的なファイルに保存します。
3.  `markitdown` ライブラリを使用して、一時ファイルをMarkdown形式に変換します。
4.  変換されたMarkdown文字列を返します。
5.  使用した一時ファイルは自動的に削除されます。

## インストール方法

このパッケージはPyPIで公開されており、pipを使って簡単にインストールできます。

```bash
pip install lynxkit-markdown
````

これにより、パッケージ本体と、依存関係にあるライブラリ (`requests`, `markitdown`) が自動的にインストールされます。

## 使い方

Pythonスクリプトから `lynxkit_markdown` パッケージをインポートし、`get_markdown_from_url()` 関数を使用します。

```python
import lynxkit_markdown

# Markdownに変換したいURLを指定
target_url = "[http://example.com](http://example.com)" # URLを文字列で指定してください

# 関数を呼び出してMarkdownを取得
markdown_content = lynxkit_markdown.get_markdown_from_url(target_url)

# 結果を確認
if markdown_content:
    print("--- Markdown変換結果 ---")
    print(markdown_content)
    print("-----------------------")

    # ファイルに保存する場合 (例)
    # try:
    #     with open("output.md", "w", encoding="utf-8") as f:
    #         f.write(markdown_content)
    #     print("\n結果を output.md に保存しました。")
    # except IOError as e:
    #     print(f"\nファイルへの保存中にエラーが発生しました: {e}")

else:
    # HTMLの取得や変換に失敗した場合
    print(f"URL ({target_url}) からMarkdownへの変換に失敗しました。")

```

`get_markdown_from_url()` 関数は、処理が成功した場合は変換されたMarkdown文字列を、何らかの理由で失敗した（URLにアクセスできない、変換に失敗したなど）場合は `None` を返します。

## 注意点

  * **変換品質:** HTMLからMarkdownへの変換品質は、内部で使用している `markitdown` ライブラリの性能に依存します。特に複雑なHTML構造やJavaScriptで動的に生成されるコンテンツの場合、期待通りに変換されないことがあります。
  * **開発ステータス:** これは主に個人用に開発されたツールです。基本的な機能は動作しますが、積極的なメンテナンスやサポートは保証されていません。バグや改善点に気づいた場合はIssue等で報告いただけると嬉しいですが、対応は不定期になる可能性があります。（気が向いたら治します！）

## 依存関係

  * Python 3.8 以降 (テスト環境: Python 3.13)
  * `requests`: URLからのHTML取得に使用
  * `markitdown`: HTMLからMarkdownへの変換に使用

これらの依存関係は `pip install lynxkit-markdown` を実行する際に自動的にインストールされます。(`pyproject.toml` に基づき解決されます。)

## ライセンス

このプロジェクトは [MITライセンス](https://www.google.com/search?q=LICENSE) の下で公開されています。詳細は `LICENSE` ファイルをご覧ください。
