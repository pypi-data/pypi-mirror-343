# lynxkit_markdown/fetcher.py
import requests # URLアクセスに必要
import sys      # エラーメッセージ出力用
from typing import Optional

def fetch_html_content(url: str) -> Optional[str]:
    """
    指定されたURLにアクセスし、そのページのHTMLコンテンツを取得して文字列として返します。

    Args:
        url (str): HTMLコンテンツを取得したいウェブページのURL。

    Returns:
        Optional[str]: 取得したHTMLコンテンツの文字列。
                       取得に失敗した場合はNoneを返します。
                       (例: ネットワークエラー, 4xx/5xxエラー, タイムアウトなど)
    """
    print(f"DEBUG [fetch_html_content]: Attempting to fetch HTML from URL: {url}")
    try:
        # --- リクエストの準備 ---
        # 一部のウェブサイトはブラウザからのアクセスでないと拒否するため、
        # 一般的なブラウザの User-Agent ヘッダーを設定します。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', # Acceptヘッダも追加するとよりブラウザらしい
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8', # 言語設定
        }

        # --- URLへのアクセス実行 ---
        # requests.get() を使用してHTTP GETリクエストを送信します。
        # timeoutパラメータで、指定秒数内に応答がない場合にタイムアウトエラーとします。
        # (接続確立とデータ受信の合計時間)
        response = requests.get(url, headers=headers, timeout=20) # 20秒でタイムアウト

        # --- レスポンスのチェック ---
        # ステータスコードが 4xx (例: 404 Not Found) または 5xx (例: 500 Server Error) の場合、
        # HTTPError例外を発生させます。これにより、エラーレスポンスを正常なHTMLと区別します。
        response.raise_for_status()

        # (オプション) Content-Typeヘッダーを確認し、HTMLでない場合に警告を表示します。
        # これは変換の精度に影響する場合があるためです。
        content_type = response.headers.get('content-type', '').lower()
        if 'html' not in content_type:
            # text/plain や application/json などが返ってきた場合
            print(f"警告 [fetch_html_content]: URL '{url}' のContent-TypeがHTMLではないようです ({content_type})。", file=sys.stderr)
            # Content-Typeが違っても、とりあえず内容を返すことにします。
            # 必要であれば、ここでNoneを返したり、例外を発生させることも可能です。

        # --- HTMLコンテンツの取得と返却 ---
        # レスポンスボディをテキスト(文字列)として取得します。
        # requestsは文字エンコーディングを自動判別しようとしますが、
        # 文字化けする場合は response.encoding を明示的に設定する必要があるかもしれません。
        html_text = response.text
        print(f"DEBUG [fetch_html_content]: Successfully fetched HTML content (length: {len(html_text)}).")
        # 取得したHTML文字列を返す
        return html_text

    # === エラーハンドリング ===
    except requests.exceptions.Timeout:
        # 指定時間内にサーバーから応答がなかった場合
        print(f"エラー [fetch_html_content]: URL '{url}' へのアクセスがタイムアウトしました (timeout={response.request.timeout if hasattr(response, 'request') else 'N/A'}s)。", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        # response.raise_for_status() が4xx/5xxエラーを検出した場合
        print(f"エラー [fetch_html_content]: URL '{url}' でHTTPエラーが発生しました: {e.response.status_code} {e.response.reason}", file=sys.stderr)
        return None
    except requests.exceptions.ConnectionError as e:
        # DNS解決ができない、サーバーに接続拒否されたなど、ネットワークレベルの問題
        print(f"エラー [fetch_html_content]: URL '{url}' への接続に失敗しました。ネットワーク接続を確認してください。詳細: {e}", file=sys.stderr)
        return None
    except requests.exceptions.InvalidSchema as e:
         # URLのスキーマ(http://, https:// など)が無効な場合
         print(f"エラー [fetch_html_content]: URL '{url}' の形式(スキーマ)が無効です: {e}", file=sys.stderr)
         return None
    except requests.exceptions.MissingSchema as e:
         # URLにスキーマが含まれていない場合 (例: "example.com")
         print(f"エラー [fetch_html_content]: URL '{url}' にスキーマ(http:// or https://)が含まれていません: {e}", file=sys.stderr)
         return None
    except requests.exceptions.RequestException as e:
        # 上記以外のrequestsライブラリ関連のエラー (例: リダイレクトが多すぎるなど)
        print(f"エラー [fetch_html_content]: URL '{url}' の取得中にリクエスト関連のエラーが発生しました: {e}", file=sys.stderr)
        return None
    except Exception as e:
        # その他の予期せぬエラー (メモリ不足など、通常は稀)
        print(f"エラー [fetch_html_content]: HTML取得中に予期せぬエラーが発生しました ({url}): {e}", file=sys.stderr)
        return None

# --- このファイルを直接実行した場合の簡単な動作確認用コード ---
if __name__ == '__main__':
    # テストしたいURLのリスト
    test_urls_list = [
        "http://example.com",              # 正常系
        "https://www.google.com",          # 正常系 (複雑なHTML)
        "https://httpbin.org/status/404",  # 404エラー
        "https://httpbin.org/status/500",  # 500エラー
        "http://domain.invalid/",          # 存在しないドメイン
        "htp://example.com",             # 無効なスキーマ
        "https://httpbin.org/delay/3"      # 3秒遅延 (タイムアウトしないはず)
    ]

    print("--- fetch_html_content 関数の動作確認 ---")
    for test_url in test_urls_list:
        print(f"\n>>> Testing URL: {test_url}")
        fetched_html = fetch_html_content(test_url)
        if fetched_html:
            # 取得成功した場合、最初の300文字程度を表示
            print(f"取得成功 (最初の300文字):\n{fetched_html[:300]}...\n")
        else:
            # 取得失敗した場合
            print("取得失敗。\n")
