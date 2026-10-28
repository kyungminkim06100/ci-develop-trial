"""장난감 원장: 잔액 이체 계산과, 그 결과를 Postgres에 쓰는 SQL을 만든다."""


def transfer(balances, src, dst, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if balances.get(src, 0) < amount:
        raise ValueError("insufficient balance")
    out = dict(balances)
    out[src] -= amount
    out[dst] = out.get(dst, 0) + amount
    return out


def upsert_sql(balances):
    rows = ", ".join(f"('{k}', {v})" for k, v in sorted(balances.items()))
    return (
        f"INSERT INTO balances(acct, amount) VALUES {rows} "
        "ON CONFLICT (account) DO UPDATE SET amount = EXCLUDED.amount;"
    )
