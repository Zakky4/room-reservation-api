# 会議室予約システム API

FastAPIとStreamlitを使用した会議室予約管理システムです。このプロジェクトは、Udemyの「Python FastAPI」コースを通じて学習・実装した内容をまとめたものです。

## 📚 コースで学んだこと

### 1. FastAPIの基礎
- **FastAPIフレームワーク**の基本概念と特徴
- RESTful APIの設計と実装
- 非同期処理（async/await）の活用
- 自動生成されるAPIドキュメント（Swagger UI）

### 2. データベース操作
- **SQLAlchemy ORM**を使用したデータベース操作
- モデルの定義とリレーションシップ
- セッション管理と依存性注入（Dependency Injection）
- SQLiteデータベースの設定と操作

### 3. データバリデーション
- **Pydantic**を使用したスキーマ定義
- リクエスト/レスポンスの型安全性
- フィールドバリデーション（最大文字数、型チェックなど）
- モデル設定（`from_attributes`）の活用

### 4. CRUD操作の実装
- Create（作成）、Read（読み取り）操作の実装
- データベースクエリの最適化（offset、limit）
- 重複チェックとエラーハンドリング
- HTTPステータスコードの適切な使用

### 5. フロントエンド連携
- **Streamlit**を使用したシンプルなUI実装
- FastAPIバックエンドとのHTTP通信
- フォーム処理とデータ表示
- エラーハンドリングとユーザーフィードバック

### 6. ビジネスロジックの実装
- 予約の重複チェック（時間帯の衝突検出）
- 定員チェック（予約人数が会議室の定員を超えないか）
- 利用時間の制限（9:00-20:00）
- データ整合性の保証

## 🏗️ アプリケーション構成

### バックエンド（FastAPI）

#### ディレクトリ構造
```
sql_app/
├── __init__.py
├── main.py          # FastAPIアプリケーションのエントリーポイント
├── models.py        # SQLAlchemyモデル定義
├── schemas.py       # Pydanticスキーマ定義
├── crud.py          # CRUD操作の実装
└── database.py      # データベース接続設定
```

#### 主要コンポーネント

**1. データベースモデル（models.py）**
- `User`: ユーザー情報（user_id, username）
- `Room`: 会議室情報（room_id, room_name, capacity）
- `Booking`: 予約情報（booking_id, user_id, room_id, booked_num, start_datetime, end_datetime）

**2. Pydanticスキーマ（schemas.py）**
- `UserCreate` / `User`: ユーザー作成・レスポンス用スキーマ
- `RoomCreate` / `Room`: 会議室作成・レスポンス用スキーマ
- `BookingCreate` / `Booking`: 予約作成・レスポンス用スキーマ

**3. CRUD操作（crud.py）**
- `get_users()` / `get_rooms()` / `get_bookings()`: 一覧取得
- `create_user()` / `create_room()` / `create_booking()`: 作成処理
- 重複チェックとエラーハンドリング

**4. APIエンドポイント（main.py）**
- `GET /users`: ユーザー一覧取得
- `POST /users`: ユーザー登録
- `GET /rooms`: 会議室一覧取得
- `POST /rooms`: 会議室登録
- `GET /bookings`: 予約一覧取得
- `POST /bookings`: 予約登録

### フロントエンド（Streamlit）

**app.py** に以下の3つのページを実装：

1. **ユーザー登録画面**
   - ユーザー名の入力と登録
   - 重複チェックとエラー表示

2. **会議室登録画面**
   - 会議室名と定員の入力と登録
   - 重複チェックとエラー表示

3. **予約登録画面**
   - 会議室一覧の表示（DataFrame形式）
   - 予約一覧の表示（DataFrame形式）
   - 予約フォーム（ユーザー選択、会議室選択、予約人数、日時入力）
   - バリデーション（定員チェック、時間チェック、重複チェック）

## 🚀 セットアップと実行方法

### 必要な環境
- Python 3.13
- pip

### インストール

1. リポジトリをクローンまたはダウンロード
```bash
cd room-reservation-api
```

2. 仮想環境の作成と有効化（推奨）
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows
```

3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 実行方法

#### 1. FastAPIサーバーの起動

```bash
uvicorn sql_app.main:app --reload
```

サーバーが起動すると、以下のURLでアクセスできます：
- API: http://127.0.0.1:8000
- APIドキュメント（Swagger UI）: http://127.0.0.1:8000/docs
- 代替APIドキュメント（ReDoc）: http://127.0.0.1:8000/redoc

#### 2. Streamlitアプリケーションの起動

別のターミナルで以下を実行：

```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 が自動的に開きます。

## 📊 データベース

- **データベース**: SQLite
- **ファイル名**: `sql_app.db`
- **テーブル**: `users`, `rooms`, `bookings`

データベースは初回実行時に自動的に作成されます。

## 🔍 主な機能

### ユーザー管理
- ユーザー名の登録（最大12文字）
- ユーザー名の重複チェック
- ユーザー一覧の取得

### 会議室管理
- 会議室名と定員の登録（会議室名は最大12文字）
- 会議室名の重複チェック
- 会議室一覧の取得

### 予約管理
- 予約の登録（ユーザー、会議室、予約人数、開始時刻、終了時刻）
- 予約の重複チェック（同じ会議室で時間帯が重複しないか）
- 定員チェック（予約人数が会議室の定員を超えないか）
- 利用時間チェック（9:00-20:00の範囲内か）
- 開始時刻と終了時刻の妥当性チェック
- 予約一覧の取得

## 🛠️ 使用技術

### バックエンド
- **FastAPI** (0.104.1): モダンなPython Webフレームワーク
- **SQLAlchemy** (2.0.25+): ORM（Object-Relational Mapping）
- **Pydantic** (2.0.0+): データバリデーション
- **Uvicorn**: ASGIサーバー

### フロントエンド
- **Streamlit** (1.28.1): PythonベースのWebアプリケーションフレームワーク

### データベース
- **SQLite**: 軽量なリレーショナルデータベース

### その他
- **requests** (2.31.0): HTTPリクエストライブラリ

## 📝 API仕様

### エンドポイント一覧

#### ユーザー関連
- `GET /users`: ユーザー一覧取得
  - クエリパラメータ: `skip` (デフォルト: 0), `limit` (デフォルト: 100)
  - レスポンス: ユーザーオブジェクトの配列

- `POST /users`: ユーザー登録
  - リクエストボディ: `{"username": "string"}`
  - レスポンス: 作成されたユーザーオブジェクト
  - エラー: 400 (ユーザー名が既に登録されている場合)

#### 会議室関連
- `GET /rooms`: 会議室一覧取得
  - クエリパラメータ: `skip` (デフォルト: 0), `limit` (デフォルト: 100)
  - レスポンス: 会議室オブジェクトの配列

- `POST /rooms`: 会議室登録
  - リクエストボディ: `{"room_name": "string", "capacity": int}`
  - レスポンス: 作成された会議室オブジェクト
  - エラー: 400 (会議室名が既に登録されている場合)

#### 予約関連
- `GET /bookings`: 予約一覧取得
  - クエリパラメータ: `skip` (デフォルト: 0), `limit` (デフォルト: 100)
  - レスポンス: 予約オブジェクトの配列

- `POST /bookings`: 予約登録
  - リクエストボディ: `{"user_id": int, "room_id": int, "booked_num": int, "start_datetime": "ISO形式の日時", "end_datetime": "ISO形式の日時"}`
  - レスポンス: 作成された予約オブジェクト
  - エラー: 404 (指定の時間帯に既に予約が入っている場合)

## 🎯 学習のポイント

### 1. 依存性注入（Dependency Injection）
FastAPIの`Depends`を使用して、データベースセッションを各エンドポイントに注入することで、コードの再利用性とテスタビリティを向上させています。

### 2. 型安全性
Pydanticスキーマを使用することで、リクエストとレスポンスの型を明確に定義し、実行時エラーを防いでいます。

### 3. エラーハンドリング
適切なHTTPステータスコードとエラーメッセージを返すことで、APIの使いやすさを向上させています。

### 4. ビジネスロジックの分離
CRUD操作を`crud.py`に分離することで、ビジネスロジックとAPIルーティングを明確に分けています。

### 5. データ整合性
データベースレベルでの制約（外部キー、ユニーク制約）とアプリケーションレベルでのバリデーションを組み合わせて、データの整合性を保証しています。

## 🔮 今後の拡張可能性

- 認証・認可機能の追加（JWT、OAuth2）
- 予約の更新・削除機能
- 予約の検索・フィルタリング機能
- ユーザー・会議室の更新・削除機能
- 予約通知機能（メール、Slackなど）
- データベースのマイグレーション機能（Alembic）
- ユニットテスト・統合テストの追加
- Docker化とデプロイメント設定
- PostgreSQLなど本番環境向けデータベースへの移行

## 📖 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://www.sqlalchemy.org/)
- [Pydantic公式ドキュメント](https://docs.pydantic.dev/)
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)

## 📄 ライセンス

このプロジェクトは学習目的で作成されたものです。

