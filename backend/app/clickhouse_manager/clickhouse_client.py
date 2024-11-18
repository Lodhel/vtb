from backend.app.config import CLICKHOUSE_URL


class ClickHouseClient:
    def __init__(self):
        self.url = CLICKHOUSE_URL
