from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    password = Column(String, nullable=True)
    phone_number = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    vtb_auth = Column(String(255))
    token_auth = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    sms_code = Column(String, default='0000')


# Модель для цели по инфляции
class InflationGoal(Base):
    __tablename__ = 'inflation_goals'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    rate_value = Column(Float, nullable=False)


# Модель для данных по инфляции
class InflationData(Base):
    __tablename__ = 'inflation_data'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    rate_value = Column(Float, nullable=False)
    period = Column(String, nullable=True)


# Модель для ключевой ставки
class KeyRate(Base):
    __tablename__ = 'key_rates'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    rate_value = Column(Float, nullable=False)
    rate_change_date = Column(Date, nullable=True)
    next_meeting_date = Column(Date, nullable=True)


# Модель для ставок межбанковского кредитного рынка
class InterbankRate(Base):
    __tablename__ = 'interbank_rates'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    rate_name = Column(String, nullable=False)
    rate_today = Column(String, nullable=True)
    rate_tomorrow = Column(String, nullable=True)


# Модель для курсов валют
class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    currency_name = Column(String, nullable=False)
    rate_today = Column(Float, nullable=True)
    rate_tomorrow = Column(Float, nullable=True)


# Модель для учетных цен на драгоценные металлы
class MetalPrice(Base):
    __tablename__ = 'metal_prices'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    metal_name = Column(String, nullable=False)
    price_today = Column(Float, nullable=True)
    price_tomorrow = Column(Float, nullable=True)


# Модель для международных резервов РФ
class Reserve(Base):
    __tablename__ = 'reserves'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    rate_date = Column(Date, nullable=True)
    reserve_value = Column(Float, nullable=True)


# Модель для показателей ликвидности банковского сектора
class LiquidityIndicator(Base):
    __tablename__ = 'liquidity_indicators'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    indicator_name = Column(String, nullable=False)
    rate_value = Column(Float, nullable=True)


# Модель для требований Банка России к кредитным организациям
class BankRequirement(Base):
    __tablename__ = 'bank_requirements'

    id = Column(Integer, primary_key=True)
    is_date = Column(Date, nullable=False)
    requirement_name = Column(String, nullable=False)
    rate_value = Column(Float, nullable=True)


class CarModel(Base):
    __tablename__ = 'car_models'

    id = Column(Integer, primary_key=True)
    model_car = Column(String)
    year = Column(Integer)
    transmission_type = Column(String)
    body_type = Column(String)
    fuel_type = Column(String)
    average_price = Column(Float)
    status = Column(String)
