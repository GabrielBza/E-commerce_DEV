from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Arquivo que define os modelos de entrada e saída dos pedidos


def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class PedidoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_consumidor: str = Field(..., min_length=1, max_length=32)
    status: str = Field(..., min_length=1, max_length=50)
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, max_length=10)

    @field_validator("id_consumidor", "status", mode="before")
    @classmethod
    def strip_string_obrigatoria(cls, value: Optional[str]) -> str:
        value = normalizar_string(value)
        if value is None:
            raise ValueError("Campo obrigatório não pode ser vazio.")
        return value

    @field_validator("entrega_no_prazo", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)

    @field_validator(
        "tempo_entrega_dias",
        "tempo_entrega_estimado_dias",
        "diferenca_entrega_dias",
    )
    @classmethod
    def validar_numeros(cls, value: Optional[float]) -> Optional[float]:
        return value


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_consumidor: Optional[str] = Field(None, min_length=1, max_length=32)
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, max_length=10)

    @field_validator("id_consumidor", "status", "entrega_no_prazo", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_pedido: str
    id_consumidor: str
    status: str
    pedido_compra_timestamp: Optional[datetime]
    pedido_entregue_timestamp: Optional[datetime]
    data_estimada_entrega: Optional[date]
    tempo_entrega_dias: Optional[float]
    tempo_entrega_estimado_dias: Optional[float]
    diferenca_entrega_dias: Optional[float]
    entrega_no_prazo: Optional[str]