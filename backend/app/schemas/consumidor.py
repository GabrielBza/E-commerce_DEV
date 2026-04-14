from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Arquivo que define os modelos de entrada e saída dos consumidores


def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class ConsumidorBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prefixo_cep: str = Field(..., min_length=1, max_length=10)
    nome_consumidor: str = Field(..., min_length=1, max_length=255)
    cidade: str = Field(..., min_length=1, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)

    @field_validator("prefixo_cep", "nome_consumidor", "cidade", "estado", mode="before")
    @classmethod
    def strip_string_obrigatoria(cls, value: Optional[str]) -> str:
        value = normalizar_string(value)
        if value is None:
            raise ValueError("Campo obrigatório não pode ser vazio.")
        return value

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value: str) -> str:
        return value.upper()


class ConsumidorCreate(ConsumidorBase):
    pass


class ConsumidorUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prefixo_cep: Optional[str] = Field(None, min_length=1, max_length=10)
    nome_consumidor: Optional[str] = Field(None, min_length=1, max_length=255)
    cidade: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)

    @field_validator("prefixo_cep", "nome_consumidor", "cidade", "estado", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.upper()


class ConsumidorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_consumidor: str
    prefixo_cep: str
    nome_consumidor: str
    cidade: str
    estado: str