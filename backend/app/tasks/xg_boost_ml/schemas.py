from dataclasses import dataclass


@dataclass
class DepositSchema:
    income: int           # Пример дохода
    expense: int          # Пример расходов
    count_child: int      # Например, 1 ребенок
    curs_dollar: int      # Курс доллара
    curs_euro: int        # Курс евро
    curs_uan: int         # Курс юаня
    oil_brent: int        # Цена на нефть Brent
    rate: int             # Процентная ставка
    inf: int              # Уровень инфляции
    education: str        # Уровень образования (категориальный признак)
    work: str             # Вид работы (категориальный признак)
    married: bool         # Семейное положение (категориальный признак)
    year: int             # Год (если хотите его использовать)
    month: int            # Месяц (если хотите его использовать)
