# Incident Briefing API

障害報告を保存し、AIで暫定原因・顧客影響・次アクションを要約するオンコール向けバックエンドです。

## 設計思想

SRE業務では速報性と再現性が重要なので、原文を保存しつつAI要約を別レコードで管理します。運用系システムらしい監査性を説明できます。

### なぜこの設計にしたのか

- ルーティング、ユースケース、永続化、AI呼び出しを分離して、責務を明確にするため。
- `mock` と `openai` を切り替えられるようにして、ローカル開発と本番連携を両立するため。
- 解析結果を元データと別テーブルで持ち、再生成と監査をしやすくするため。
- 認証、例外整形、入力制約を最初から入れ、実務に近い非機能要件まで示すため。

## 技術スタック

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- SQLite（`DATABASE_URL` を差し替えれば Postgres に移行可能）
- OpenAI互換API / mock provider
- Pytest / Ruff / Black / Mypy
- Docker / GitHub Actions

## ディレクトリ構成

```text
.
├── .env.example
├── .github/workflows/ci.yml
├── app
│   ├── api/routes.py
│   ├── core/config.py
│   ├── core/errors.py
│   ├── core/security.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services
│       ├── ai.py
│       └── domain.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── README.md
└── tests
    ├── conftest.py
    ├── test_health.py
    └── test_workflow.py
```

## API概要

- `POST /incidents`: 障害レポートを登録
- `GET /incidents/{id}`: 障害レポートを取得
- `POST /incidents/{id}/brief`: AI解析を実行
- `GET /incidents/{id}/briefing`: 解析結果を取得

## 最小実装コード例

```python
@router.post(
    "/incidents/{record_id}/brief",
    response_model=schemas.IncidentBriefingResponse,
    dependencies=[Depends(verify_internal_api_key)],
)
def analyze_record(
    record_id: str,
    service: IncidentService = Depends(get_service),
) -> schemas.IncidentBriefingResponse:
    return service.brief_incident(record_id)
```

## ローカル起動

```bash
cp .env.example .env
make install
make run
```

Dockerでも起動できます。

```bash
cp .env.example .env
docker compose up --build
```

デフォルトでは `AI_PROVIDER=mock` のため、外部AIキーなしで動作確認できます。

## テスト

```bash
make test
make lint
make typecheck
```

## セキュリティ配慮

- 障害情報は機密度が高いため、書き込み・参照APIを内部キー前提に絞る。
- AI出力は自由文ではなくJSONバリデーション済み構造体として保存し、運用チャットへ転送しやすくする。
- トレースや秘密情報をそのまま外部送信しないよう、投入データの要約前処理を挟みやすい構造にしている。

## エラーハンドリング設計

- AI失敗時は 502 を返して原因を切り分けしやすくする。
- DB失敗時はロールバックして再試行可能な状態に保つ。

## CI

GitHub Actions で以下を実行します。

- `ruff check .`
- `black --check .`
- `mypy app tests`
- `pytest`

## サンプルリクエスト

```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -H "X-Internal-API-Key: dev-internal-key" \
  -d '{
  "service_name": "checkout-api",
  "alert_summary": "5xx rate exceeded threshold",
  "timeline": "09:02 API latency spiked. 09:05 checkout started returning 502. 09:12 rollback initiated."
}'
```

## READMEテンプレとして使う場合の章立て

- 背景 / 課題設定
- コンセプト
- 設計思想
- 技術スタック
- ディレクトリ構成
- ローカル起動手順
- API仕様
- テスト / CI
- セキュリティ
- 今後の拡張
