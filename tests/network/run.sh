#!/usr/bin/env bash
# 실제 Postgres에 이체 결과를 쓰고 다시 읽어 맞는지 본다. 단위 시험이 못 보는 것(SQL이 실제로 도는지)을 본다.
set -euo pipefail
export PGPASSWORD=postgres
q() { psql -h localhost -U postgres -v ON_ERROR_STOP=1 -tA -c "$1"; }

q "CREATE TABLE IF NOT EXISTS balances(account text PRIMARY KEY, amount int NOT NULL CHECK (amount >= 0));"
sql=$(python3 -c 'import sys; sys.path.insert(0, "src")
from ledger import transfer, upsert_sql
print(upsert_sql(transfer({"a": 10}, "a", "b", 3)))')
q "$sql"
got=$(q "SELECT string_agg(account || '=' || amount, ',' ORDER BY account) FROM balances;")
[ "$got" = "a=7,b=3" ] || { echo "expected a=7,b=3, got $got"; exit 1; }

# 망 시험이 오래 걸리는 상황을 흉내 낸다(쌓인 머지가 한 번에 시험되는지 보려고).
sleep "${NETWORK_SLEEP:-60}"
echo "network ok: $got"
