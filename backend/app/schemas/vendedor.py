from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Arquivo que define os modelos de entrada e saída dos vendedores


def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class VendedorBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_vendedor: str = Field(..., min_length=1, max_length=255)
    prefixo_cep: str = Field(..., min_length=1, max_length=10)
    cidade: str = Field(..., min_length=1, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)

    @field_validator("nome_vendedor", "prefixo_cep", "cidade", "estado", mode="before")
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


class VendedorCreate(VendedorBase):
    pass


class VendedorUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_vendedor: Optional[str] = Field(None, min_length=1, max_length=255)
    prefixo_cep: Optional[str] = Field(None, min_length=1, max_length=10)
    cidade: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)

    @field_validator("nome_vendedor", "prefixo_cep", "cidade", "estado", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.upper()


class VendedorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_vendedor: str
    nome_vendedor: str
    prefixo_cep: str
    cidade: str
    estado: str