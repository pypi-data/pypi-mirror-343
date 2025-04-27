# lynxkit_markdown/core.py
import sys
from typing import Optional

# これまで作成したモジュールから必要な関数をインポート
# 相対インポート (. から始める) を使用
from .fetcher import fetch_html_content
from .html_processor import convert_html_string_to_md_via_temp_file

def get_markdown_from_url(url: str) -> Optional[str]:
    """
    URLを受け取り、HTMLを取得し、それをMarkdownに変換して返す、
    このパッケージの主要なエントリーポイント関数です。

    Args:
        url (str): Markdownに変換したいページのURL。

    Returns:
        Optional[str]: 変換されたMarkdown文字列。
                       途中の処理（HTML取得、Markdown変換）のいずれかで
                       失敗した場合はNoneを返します。
    """
    print(f"INFO [core.get_markdown_from_url]: Processing URL: {url}")

    # === ステップ 1: URLからHTMLコンテンツを取得 ===
    # fetcherモジュールの関数を呼び出す
    print("DEBUG [core.get_markdown_from_url]: Calling fetch_html_content...")
    html_content = fetch_html_content(url)

    # HTML取得に失敗した場合 (fetch_html_contentがNoneを返した場合)
    if html_content is None:
        # fetch_html_content内でエラーメッセージは出力されているはず
        print(f"エラー [core.get_markdown_from_url]: Failed to fetch HTML from URL: {url}", file=sys.stderr)
        # 処理を中断し、Noneを返す
        return None

    print(f"DEBUG [core.get_markdown_from_url]: HTML fetched successfully (length: {len(html_content)}).")

    # === ステップ 2: 取得したHTML文字列をMarkdownに変換 ===
    # html_processorモジュールの関数を呼び出す (一時ファイル経由)
    print("DEBUG [core.get_markdown_from_url]: Calling convert_html_string_to_md_via_temp_file...")
    markdown_output = convert_html_string_to_md_via_temp_file(html_content)

    # Markdown変換に失敗した場合 (convert...がNoneを返した場合)
    if markdown_output is None:
        # convert_html_string_to_md_via_temp_file内でエラーメッセージは出力されているはず
        print(f"エラー [core.get_markdown_from_url]: Failed to convert HTML to Markdown for URL: {url}", file=sys.stderr)
        # 処理を中断し、Noneを返す
        return None

    # === 成功した場合 ===
    print(f"INFO [core.get_markdown_from_url]: Successfully processed URL and converted to Markdown (length: {len(markdown_output)}).")
    # 最終的なMarkdown文字列を返す
    return markdown_output

# --- このファイルを直接実行した場合の簡単な動作確認用コード ---
if __name__ == '__main__':
    # テストしたいURLをいくつか試す
    urls_to_test = [
        "http://example.com",
        "https://info.cern.ch/hypertext/WWW/TheProject.html", # シンプルなHTML
        "https://httpbin.org/status/404",                     # 失敗例(404)
        "http://invalid.domain.fsfdsfdsf"                     # 失敗例(接続エラー)
    ]

    print("--- get_markdown_from_url 関数の動作確認 (Direct Run) ---")
    for test_url in urls_to_test:
        print(f"\n>>> Processing URL: {test_url}")
        final_markdown_result = get_markdown_from_url(test_url)

        if final_markdown_result:
            print("\n--- 変換成功 ---")
            print("Markdown (最初の500文字):")
            print(final_markdown_result[:500])
            if len(final_markdown_result) > 500:
                print("...")
            print("-" * 30)
        else:
            print("\n--- 変換失敗 ---")
            print("-" * 30)
