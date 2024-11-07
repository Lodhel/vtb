import datetime

from fastapi import Query


class CbrParams:
    def __init__(
        self,
        rate_date: str = Query(default=datetime.date.today(), description="информация по дате")
    ):
        self.rate_date = rate_date
