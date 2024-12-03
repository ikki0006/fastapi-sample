

## 初回対応
venvの作成が安定しないので仮想環境に入っていない場合は下記コマンドを実行
(仮想環境外でも動くようにはしている)
```
uv venv
source .venv/bin/activate
```

### 起動コマンド
uvicorn app.main:app --reload --log-config log_conf.yml


