# tests/test_core.py
import pytest

# --- テスト対象の関数をインポート ---
try:
    # エントリーポイント関数をインポート
    from lynxkit_markdown.core import get_markdown_from_url
    # 依存関係の利用可能性を確認 (html_processorから)
    from lynxkit_markdown.html_processor import markitdown_available
except ImportError as e:
    pytest.fail(f"Failed to import modules/functions for core tests: {e}", pytrace=False)
    # ダミー定義
    def get_markdown_from_url(*args, **kwargs): return None
    markitdown_available = False

# --- pytestマーカー ---
# 依存ライブラリ(markitdown)が利用できない場合はテストをスキップ
skip_if_dependencies_unavailable = pytest.mark.skipif(
    not markitdown_available,
    reason="Required dependencies (like markitdown) are not available"
)
# ネットワークアクセスが必要なテスト用のマーカー
requires_network = pytest.mark.network

# --- テスト用のURL定義 ---
VALID_URL_EXAMPLE = "http://example.com"
VALID_URL_CERN = "https://info.cern.ch/hypertext/WWW/TheProject.html" # シンプルなHTML
URL_RETURNS_404 = "https://httpbin.org/status/404"
URL_INVALID_DOMAIN = "http://domain-that-does-not-exist-kjhgf.com"

# --- テスト関数 ---

@skip_if_dependencies_unavailable
@requires_network
def test_integration_valid_url_example():
    """有効なURL(example.com)で最終的なMarkdownが取得できるか (統合テスト)"""
    print(f"\n--- Testing get_markdown_from_url (integration) with: {VALID_URL_EXAMPLE} ---")
    markdown = get_markdown_from_url(VALID_URL_EXAMPLE)
    assert markdown is not None, "有効なURLでNoneが返ってはならない"
    assert isinstance(markdown, str), "結果は文字列であるべき"
    assert len(markdown) > 0, "結果は空文字列であってはならない"
    # example.comの場合、markitdownの出力に依存するが、基本的なテキストが含まれるか確認
    assert "Example Domain" in markdown, "Expected text 'Example Domain' not found in result"
    print(f"--- Integration test with example.com PASSED (returned Markdown length: {len(markdown)}) ---")

@skip_if_dependencies_unavailable
@requires_network
def test_integration_valid_url_cern():
    """有効なURL(info.cern.ch)で最終的なMarkdownが取得できるか (統合テスト)"""
    print(f"\n--- Testing get_markdown_from_url (integration) with: {VALID_URL_CERN} ---")
    markdown = get_markdown_from_url(VALID_URL_CERN)
    assert markdown is not None, "有効なURLでNoneが返ってはならない"
    assert isinstance(markdown, str), "結果は文字列であるべき"
    assert len(markdown) > 0, "結果は空文字列であってはならない"
    # CERNのページ内容の断片が含まれるか確認 (markitdownの変換結果に依存)
    assert "World Wide Web" in markdown or "W3" in markdown # どちらかが含まれることを期待
    print(f"--- Integration test with info.cern.ch PASSED (returned Markdown length: {len(markdown)}) ---")

@skip_if_dependencies_unavailable
@requires_network
def test_integration_404_url():
    """404エラーのURLで最終的にNoneが返るかテスト"""
    print(f"\n--- Testing get_markdown_from_url (integration) with 404 URL: {URL_RETURNS_404} ---")
    markdown = get_markdown_from_url(URL_RETURNS_404)
    # HTML取得(fetcher)の段階で失敗し、Noneが返るはず
    assert markdown is None, "404 URLでは最終的にNoneが返るべき"
    print("--- Integration test with 404 URL PASSED (returned None) ---")

@skip_if_dependencies_unavailable
@requires_network
def test_integration_invalid_domain():
    """存在しないドメインのURLで最終的にNoneが返るかテスト"""
    print(f"\n--- Testing get_markdown_from_url (integration) with invalid domain: {URL_INVALID_DOMAIN} ---")
    markdown = get_markdown_from_url(URL_INVALID_DOMAIN)
    # HTML取得(fetcher)の段階で失敗し、Noneが返るはず
    assert markdown is None, "存在しないドメインのURLでは最終的にNoneが返るべき"
    print("--- Integration test with invalid domain PASSED (returned None) ---")


# --- pytest 実行方法 ---
# (ターミナルでプロジェクトルートにて)
#
# テストを実行 (デバッグ出力あり、詳細表示):
#   pytest -v -s tests/test_core.py
#
# ネットワークアクセスを伴うテストのみ実行:
#   pytest -v -s -m network tests/test_core.py
#
