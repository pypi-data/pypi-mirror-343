# lynxkit_markdown/html_processor.py
import os
import sys
import tempfile # 一時ファイルの作成に必要
from typing import Optional

# --- markitdown ライブラリのインポートと初期化 ---
try:
    # ご指示通り markitdown をインポート
    from markitdown import MarkItDown
    # markitdownのインスタンスを生成（このモジュール内で共有）
    markitdown_converter = MarkItDown()
    markitdown_available = True # ライブラリが利用可能であることを示すフラグ
    print("DEBUG [html_processor]: MarkItDown instance created successfully.")
except ImportError:
    # ライブラリが見つからない場合
    print("エラー [html_processor]: 'markitdown' ライブラリが見つかりません。", file=sys.stderr)
    markitdown_available = False
    markitdown_converter = None # 利用できないことを示すためNoneを入れておく
except Exception as e:
    # インスタンス化中に他のエラーが発生した場合
    print(f"エラー [html_processor]: MarkItDownのインスタンス化中にエラーが発生しました: {e}", file=sys.stderr)
    markitdown_available = False
    markitdown_converter = None

def convert_html_string_to_md_via_temp_file(html_string: str) -> Optional[str]:
    """
    HTML文字列を受け取り、一時ファイルを経由して'markitdown'でMarkdownに変換します。

    Args:
        html_string (str): 変換したいHTMLコンテンツの文字列。

    Returns:
        Optional[str]: 変換されたMarkdown文字列。
                       markitdownライブラリが利用できない場合や、
                       変換に失敗した場合はNoneを返します。
    """
    # markitdownライブラリが利用可能か最初にチェック
    if not markitdown_available:
        print("エラー [html_processor]: 'markitdown' ライブラリが利用できません。", file=sys.stderr)
        return None

    # --- 入力値のチェック ---
    if not isinstance(html_string, str):
        print("エラー [html_processor]: 入力はHTML文字列である必要があります。", file=sys.stderr)
        return None
    # 空文字列や空白のみの文字列の場合、処理を中断してNoneを返す
    if not html_string.strip():
        print("エラー [html_processor]: 入力のHTML文字列が空または空白のみです。", file=sys.stderr)
        return None

    # 一時ファイルのパスを格納する変数 (finallyブロックで使うため外で定義)
    temp_file_path: Optional[str] = None
    # 変換結果のMarkdownを格納する変数
    markdown_text: Optional[str] = None

    try:
        # === ステップ 1: 一時ファイルを作成し、HTMLコンテンツを書き込む ===
        # tempfile.NamedTemporaryFile を使用
        # mode='w': 書き込みモード
        # suffix='.html': ファイル名の末尾に拡張子を付ける
        # delete=False: withブロックを抜けても自動で削除しない (手動で削除するため)
        # encoding='utf-8': 書き込み時のエンコーディング
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_f:
            temp_file_path = temp_f.name # 作成された一時ファイルのフルパスを取得
            temp_f.write(html_string)   # HTML文字列をファイルに書き込む
        # ファイルオブジェクトtemp_fはこの時点で閉じられる
        print(f"DEBUG [html_processor]: HTML string written to temp file: {temp_file_path}")

        # === ステップ 2: 一時ファイルのパスを markitdown に渡して変換 ===
        # convertメソッドはファイルパスを受け付けるはず
        result = markitdown_converter.convert(temp_file_path)
        print(f"DEBUG [html_processor]: markitdown.convert('{os.path.basename(temp_file_path)}') returned type: {type(result)}")

        # 変換結果オブジェクトから .text_content 属性を取得
        if hasattr(result, 'text_content'):
            markdown_text = result.text_content
            print(f"DEBUG [html_processor]: Successfully extracted text_content (length: {len(markdown_text)}) via temp file.")
        else:
            # 予期しない形式のオブジェクトが返ってきた場合
            print(f"エラー [html_processor]: 'markitdown.convert'の戻り値に'text_content'属性が見つかりません。戻り値: {result}", file=sys.stderr)
            markdown_text = None # 失敗を示す

    except IOError as e:
        # 一時ファイルの作成や書き込みに失敗した場合
        print(f"エラー [html_processor]: 一時ファイルの書き込み中にエラーが発生しました: {e}", file=sys.stderr)
        markdown_text = None # 失敗を示す
    except AttributeError as e:
         # convertメソッドやtext_content属性が存在しないなど
         print(f"エラー [html_processor]: 'markitdown'ライブラリの使い方が間違っている可能性があります: {e}", file=sys.stderr)
         markdown_text = None
    except Exception as e:
        # markitdown.convert() 実行中の予期せぬエラーなど
        print(f"エラー [html_processor]: Markdown変換中に予期せぬエラーが発生しました: {e}", file=sys.stderr)
        markdown_text = None # 失敗を示す
    finally:
        # === ステップ 3: 一時ファイルを必ず削除する ===
        # temp_file_path が設定されており(一時ファイルが作られ)、かつそのファイルが存在する場合
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path) # ファイルを削除
                print(f"DEBUG [html_processor]: Temporary file removed: {temp_file_path}")
            except OSError as e:
                # ファイルがロックされているなどの理由で削除に失敗した場合
                print(f"警告 [html_processor]: 一時ファイルの削除に失敗しました: {temp_file_path} ({e})", file=sys.stderr)

    # 最終的な変換結果（成功時はMarkdown文字列、失敗時はNone）を返す
    return markdown_text

# --- このファイルを直接実行した場合の簡単な動作確認用コード ---
if __name__ == '__main__':
    sample_html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Direct Run Test</title></head>
    <body>
        <h1>動作確認</h1>
        <p>これは <code>html_processor.py</code> を直接実行した際のテストです。</p>
        <ul><li>リスト項目</li></ul>
    </body>
    </html>
    """
    print("--- Testing HTML string conversion via temp file (Direct Run) ---")
    markdown_result = convert_html_string_to_md_via_temp_file(sample_html_content)

    if markdown_result:
        print("\n--- 変換成功 ---")
        print(markdown_result)
        print("----------------")
    else:
        print("\n--- 変換失敗 ---")

    print("\n--- 無効な入力のテスト (Direct Run) ---")
    convert_html_string_to_md_via_temp_file(None) # type: ignore
    convert_html_string_to_md_via_temp_file("  ") # 空白のみ
