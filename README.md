

## 初回対応
1. envファイルを準備する
-> 環境により差分があるが見えててもいい変数は.envに。見えては行けない変数は.devcontainer/docker_envに記載する

devcontainerの拡張機能を入れて、コンテナを立ち上げる




venvの作成が安定しないので仮想環境に入っていない場合は下記コマンドを実行
```
uv venv
source .venv/bin/activate
```

その後、推奨拡張機能がすべて入っているか確認


### 起動コマンド
uvicorn app.main:app --host=0.0.0.0 --port=80 --log-config log_conf.yml --reload


### localでのdynamo確認
http://localhost:8001/
データは`./.devcontainer/dynamodb`に入る。サイズが肥大化したら削除推奨
