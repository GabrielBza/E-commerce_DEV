from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class ProdutoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_produto: str = Field(..., min_length=1, max_length=255)
    categoria_produto: str = Field(..., min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

    @field_validator("nome_produto", "categoria_produto", mode="before")
    @classmethod
    def strip_string_obrigatoria(cls, value: Optional[str]) -> str:
        value = normalizar_string(value)
        if value is None:
            raise ValueError("Campo obrigatório não pode ser vazio.")
        return value


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_produto: Optional[str] = Field(None, min_length=1, max_length=255)
    categoria_produto: Optional[str] = Field(None, min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

    @field_validator("nome_produto", "categoria_produto", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_produto: str
    nome_produto: str
    categoria_produto: str
    peso_produto_gramas: Optional[float]
    comprimento_centimetros: Optional[float]
    altura_centimetros: Optional[float]
    largura_centimetros: Optional[float]