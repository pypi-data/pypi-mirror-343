# tests/test_fetcher.py
import pytest

# --- テスト対象の関数をインポート ---
try:
    from lynxkit_markdown.fetcher import fetch_html_content
except ImportError as e:
    pytest.fail(f"Failed to import fetch_html_content from lynxkit_markdown.fetcher: {e}", pytrace=False)
    # ダミー定義
    def fetch_html_content(*args, **kwargs): return None

# --- テスト用のURL定義 ---
VALID_URL_EXAMPLE = "http://example.com"
VALID_URL_GOOGLE = "https://www.google.com" # 比較的安定しているが内容は変わりうる
URL_RETURNS_404 = "https://httpbin.org/status/404" # 確実に404を返す
URL_RETURNS_500 = "https://httpbin.org/status/500" # 確実に500を返す
URL_NON_EXISTENT_DOMAIN = "http://domain-that-does-not-exist-and-should-fail-dns.com" # DNS解決失敗を期待
URL_INVALID_SCHEMA = "ftp://example.com" # 無効なスキーマ (requestsがエラーを出すはず)
URL_MISSING_SCHEMA = "example.com"      # スキーマなし (requestsがエラーを出すはず)
URL_FOR_TIMEOUT = "https://httpbin.org/delay/30" # 30秒遅延 (fetcher内のtimeout=20秒より長い)

# --- pytestマーカー ---
# ネットワークアクセスが必要なテストにマークを付ける
requires_network = pytest.mark.network

# --- テスト関数 ---

@requires_network
def test_fetch_from_valid_url_example():
    """有効なURL(example.com)からHTMLが取得できるか"""
    print(f"\n--- Testing fetch from valid URL: {VALID_URL_EXAMPLE} ---")
    html = fetch_html_content(VALID_URL_EXAMPLE)
    assert html is not None, "有効なURLからNoneが返ってはならない"
    assert isinstance(html, str), "取得結果は文字列であるべき"
    assert len(html) > 0, "取得結果は空文字列であってはならない"
    # example.com の内容が含まれているか簡易チェック
    assert "<title>Example Domain</title>" in html, "Expected title tag not found"
    assert "<h1>Example Domain</h1>" in html, "Expected h1 tag not found"
    print("--- Fetch from example.com PASSED ---")

@requires_network
def test_fetch_from_valid_url_google():
    """有効なURL(google.com)からHTMLが取得できるか"""
    print(f"\n--- Testing fetch from valid URL: {VALID_URL_GOOGLE} ---")
    html = fetch_html_content(VALID_URL_GOOGLE)
    assert html is not None, "有効なURLからNoneが返ってはならない"
    assert isinstance(html, str), "取得結果は文字列であるべき"
    assert len(html) > 0, "取得結果は空文字列であってはならない"
    # Googleのページ内容はある程度予測可能だが変わりうるため、存在チェック程度に留める
    assert "<html" in html.lower(), "Expected <html> tag start not found"
    assert "<body" in html.lower(), "Expected <body> tag start not found"
    print("--- Fetch from google.com PASSED ---")

@requires_network
def test_fetch_from_404_url():
    """404エラーを返すURLでNoneが返るか"""
    print(f"\n--- Testing fetch from 404 URL: {URL_RETURNS_404} ---")
    html = fetch_html_content(URL_RETURNS_404)
    assert html is None, "404 URLからはNoneが返るべき (HTTPError)"
    print("--- Fetch from 404 URL PASSED (returned None) ---")

@requires_network
def test_fetch_from_500_url():
    """500エラーを返すURLでNoneが返るか"""
    print(f"\n--- Testing fetch from 500 URL: {URL_RETURNS_500} ---")
    html = fetch_html_content(URL_RETURNS_500)
    assert html is None, "500 URLからはNoneが返るべき (HTTPError)"
    print("--- Fetch from 500 URL PASSED (returned None) ---")

@requires_network
def test_fetch_from_non_existent_domain():
    """存在しないドメインのURLでNoneが返るか"""
    print(f"\n--- Testing fetch from non-existent domain: {URL_NON_EXISTENT_DOMAIN} ---")
    html = fetch_html_content(URL_NON_EXISTENT_DOMAIN)
    assert html is None, "存在しないドメインのURLからはNoneが返るべき (ConnectionError)"
    print("--- Fetch from non-existent domain PASSED (returned None) ---")

# requestsはスキーマがない/無効な場合もエラーを出す
def test_fetch_from_invalid_schema():
    """無効なスキーマ(ftp://)のURLでNoneが返るか"""
    print(f"\n--- Testing fetch from invalid schema: {URL_INVALID_SCHEMA} ---")
    html = fetch_html_content(URL_INVALID_SCHEMA)
    assert html is None, "無効なスキーマのURLからはNoneが返るべき (InvalidSchema)"
    print("--- Fetch from invalid schema PASSED (returned None) ---")

def test_fetch_from_missing_schema():
    """スキーマがないURLでNoneが返るか"""
    print(f"\n--- Testing fetch from missing schema: {URL_MISSING_SCHEMA} ---")
    html = fetch_html_content(URL_MISSING_SCHEMA)
    assert html is None, "スキーマがないURLからはNoneが返るべき (MissingSchema)"
    print("--- Fetch from missing schema PASSED (returned None) ---")

# タイムアウトテストは時間がかかるため、通常はスキップ
@pytest.mark.skip(reason="Test takes > 20 seconds, run explicitly if needed")
@requires_network
@pytest.mark.slow # pytest --runslow で実行するためのマーカー (オプション)
def test_fetch_that_timeouts():
    """タイムアウトするURLでNoneが返るか"""
    # fetch_html_content内のtimeout(20秒) < URL_FOR_TIMEOUTの遅延(30秒)
    print(f"\n--- Testing fetch timeout: {URL_FOR_TIMEOUT} ---")
    html = fetch_html_content(URL_FOR_TIMEOUT)
    assert html is None, "タイムアウトするURLからはNoneが返るべき (Timeout)"
    print("--- Fetch timeout test PASSED (returned None) ---")

# --- pytest 実行方法 ---
# (ターミナルでプロジェクトルートにて)
#
# 依存ライブラリをインストール (まだの場合):
#   pip install requests pytest
#
# テストを実行 (デバッグ出力あり、詳細表示):
#   pytest -v -s tests/test_fetcher.py
#
# ネットワークアクセスを伴うテストのみ実行:
#   pytest -v -s -m network tests/test_fetcher.py
#
# 遅いテストも含めて実行する場合（pytest.ini設定またはコマンドラインオプションが必要）:
#   pytest -v -s tests/test_fetcher.py --runslow (pytest-skip-slow プラグインなど)
#   または、テストコードの @pytest.mark.skip をコメントアウトして普通に実行
