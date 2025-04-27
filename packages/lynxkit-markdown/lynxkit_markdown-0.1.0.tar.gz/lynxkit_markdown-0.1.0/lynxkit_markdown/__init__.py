# lynxkit_markdown/__init__.py

# 他のモジュールからのインポートは必要に応じて残す or 削除する
# from .converter import ...
# from .html_processor import convert_html_string_to_md_via_temp_file # 必要なら公開
# from .fetcher import fetch_html_content # 必要なら公開

# coreモジュールからエントリーポイント関数をインポートして公開する
from .core import get_markdown_from_url

# パッケージバージョン（オプション）
# __version__ = "0.1.0"
