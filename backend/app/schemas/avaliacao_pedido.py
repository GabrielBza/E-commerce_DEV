from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Arquivo que define os modelos de entrada e saída das avaliações de pedidos
# Responsável por validar e estruturar os dados que trafegam entre o cliente e o backend


# Função simples que retorna strings após aplicação de strip ou valores nulos caso a string esteja vazia
def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class AvaliacaoPedidoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_pedido: str = Field(..., min_length=1, max_length=32)
    avaliacao: int = Field(..., ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, max_length=255)
    comentario: Optional[str] = Field(None, max_length=1000)
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None

    @field_validator("id_pedido", mode="before")
    @classmethod
    def validar_id_pedido(cls, value: Optional[str]) -> str:
        value = normalizar_string(value)
        if value is None:
            raise ValueError("Campo obrigatório não pode ser vazio.")
        return value

    @field_validator("titulo_comentario", "comentario", mode="before")
    @classmethod
    def strip_strings_opcionais(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)


class AvaliacaoPedidoCreate(AvaliacaoPedidoBase):
    pass


class AvaliacaoPedidoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    avaliacao: Optional[int] = Field(None, ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, max_length=255)
    comentario: Optional[str] = Field(None, max_length=1000)
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None

    @field_validator("titulo_comentario", "comentario", mode="before")
    @classmethod
    def strip_strings_opcionais(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)


class AvaliacaoPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_avaliacao: str
    id_pedido: str
    avaliacao: int
    titulo_comentario: Optional[str]
    comentario: Optional[str]
    data_comentario: Optional[datetime]
    data_resposta: Optional[datetime]