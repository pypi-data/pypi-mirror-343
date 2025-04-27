# tests/test_html_processor.py
import pytest
import os # テスト内では使わないが、習慣として

# --- テスト対象の関数をインポート ---
# インポートエラーも考慮
try:
    from lynxkit_markdown.html_processor import (
        convert_html_string_to_md_via_temp_file,
        markitdown_available # ライブラリが利用可能かどうかのフラグもインポート
    )
except ImportError as e:
    # モジュールのインポート自体に失敗した場合、テストを続行できない
    pytest.fail(f"Failed to import module or function from html_processor: {e}", pytrace=False)
    # ダミー定義（NameError回避のため、ただしテストはfailする）
    markitdown_available = False
    def convert_html_string_to_md_via_temp_file(*args, **kwargs): return None

# --- pytestマーカー ---
# markitdownライブラリが利用できない場合は、関連するテストをスキップする
skip_if_markitdown_unavailable = pytest.mark.skipif(
    not markitdown_available,
    reason="markitdown library is not available or failed to initialize"
)

# --- テストデータ ---
SIMPLE_VALID_HTML = """
<!DOCTYPE html>
<html>
<head><title>Simple Test</title></head>
<body>
    <h1>テスト見出し</h1>
    <p>これは<b>太字</b>と<i>斜体</i>を含む段落です。</p>
    <ul><li>リスト1</li><li>リスト2</li></ul>
</body>
</html>
"""
# 期待されるMarkdownの一部（markitdownの出力に依存するため、コメントアウトしておくか、実際の出力に合わせて調整）
# EXPECTED_MD_H1 = "# テスト見出し"
# EXPECTED_MD_P = "これは**太字**と*斜体*を含む段落です。"
# EXPECTED_MD_LI = "* リスト1"

EMPTY_HTML_STRING = ""
WHITESPACE_HTML_STRING = "   \n \t "
INVALID_INPUT_NON_STRING = 12345

# --- テスト関数 ---

@skip_if_markitdown_unavailable
def test_convert_simple_html_string_via_temp_file():
    """簡単なHTML文字列が一時ファイル経由で正しく変換されるかテスト"""
    print("\n--- Testing simple HTML string via temp file ---")
    markdown = convert_html_string_to_md_via_temp_file(SIMPLE_VALID_HTML)

    # 基本的なチェック
    assert markdown is not None, "有効なHTML文字列からの変換結果がNoneであってはならない"
    assert isinstance(markdown, str), "変換結果は文字列であるべき"
    assert len(markdown) > 0, "変換結果は空文字列であってはならない"

    # より詳細なチェック (markitdownの実際の出力を見てから調整)
    # assert EXPECTED_MD_H1 in markdown, "H1タグが正しく変換されていること"
    # assert EXPECTED_MD_P in markdown, "Pタグと強調タグが正しく変換されていること"
    # assert EXPECTED_MD_LI in markdown, "UL/LIタグが正しく変換されていること"

    print(f"--- Simple HTML string via temp file PASSED (returned string length: {len(markdown)}) ---")
    # print(f"DEBUG Output:\n{markdown}") # 必要に応じて変換結果を出力して確認

@skip_if_markitdown_unavailable
def test_convert_empty_string_input():
    """空文字列を入力した場合にNoneが返るかテスト"""
    print("\n--- Testing empty HTML string input ---")
    markdown = convert_html_string_to_md_via_temp_file(EMPTY_HTML_STRING)
    # 関数内で空文字列はNoneを返すように実装した
    assert markdown is None, "空文字列を入力した場合はNoneが返るべき"
    print("--- Empty string input test PASSED (returned None) ---")

@skip_if_markitdown_unavailable
def test_convert_whitespace_string_input():
    """空白のみの文字列を入力した場合にNoneが返るかテスト"""
    print("\n--- Testing whitespace HTML string input ---")
    markdown = convert_html_string_to_md_via_temp_file(WHITESPACE_HTML_STRING)
    # 関数内で空白のみの文字列はNoneを返すように実装した
    assert markdown is None, "空白のみの文字列を入力した場合はNoneが返るべき"
    print("--- Whitespace string input test PASSED (returned None) ---")

@skip_if_markitdown_unavailable
def test_convert_invalid_input_type():
    """文字列以外の無効な型を入力した場合にNoneが返るかテスト"""
    print("\n--- Testing invalid input type (int) ---")
    markdown = convert_html_string_to_md_via_temp_file(INVALID_INPUT_NON_STRING) # type: ignore
    assert markdown is None, "非文字列を入力した場合はNoneが返るべき"
    print("--- Invalid input type test PASSED (returned None) ---")

# --- pytest 実行方法 ---
# (ターミナルでプロジェクトルートにて)
#
# テストを実行 (デバッグ出力あり、詳細表示):
#   pytest -v -s tests/test_html_processor.py
#
