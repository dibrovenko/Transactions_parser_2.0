import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Optional

from db.models import TypeTransactionEnum


class TransactionDTO(BaseModel):
    signature: str
    mint: str
    traderPublicKey: str
    txType: TypeTransactionEnum
    solAmount: float

    tokenAmount: Optional[float] = None  # кроме create
    initialBuy: Optional[float] = None  # только create
    bondingCurveKey: Optional[str] = None  # кроме pool
    newTokenBalance: Optional[float] = None  # buy и sell
    vTokensInBondingCurve: Optional[float] = None  # кроме pool
    vSolInBondingCurve: Optional[float] = None  # кроме pool
    marketCapSol: Optional[float] = None  # кроме pool
    name: Optional[str] = None  # только create
    symbol: Optional[str] = None  # только create
    uri: Optional[str] = None  # только create
    pool: Optional[str] = None  # pump или radium

    created_at: datetime

    # Валидатор для обработки created_at
    @model_validator(mode='before')
    def set_created_at(cls, values):
        if isinstance(values, dict) and "created_at" not in values:
            values["created_at"] = datetime.now()
        return values

    # Валидатор для обработки txType == "create" (очищение имени и символа)
    @model_validator(mode='before')
    def handle_create_tx(cls, values):
        if isinstance(values, dict) and values.get('txType') == "create":
            values["name"] = values.get("name", "").replace("\x00", "")
            values["symbol"] = values.get("symbol", "").replace("\x00", "")
        return values

    class Config:
        # Config for supporting types like Enum and UUIDs.
        use_enum_values = True
        from_attributes = True



"""class TransactionDTO(BaseModel):
    signature: str
    mint: str
    traderPublicKey: str
    txType: TypeTransactionEnum
    initialBuy: float | None = None
    bondingCurveKey: str
    vTokensInBondingCurve: float
    vSolInBondingCurve: float
    marketCapSol: float
    name: str | None = None
    symbol: str | None = None
    uri: str | None = None
    created_at: datetime
    pool: str | None = None

    class Config:
        # Config for supporting types like Enum and UUIDs.
        use_enum_values = True
        from_attributes = True"""
