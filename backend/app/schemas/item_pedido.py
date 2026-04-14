from pydantic import BaseModel, ConfigDict, Field


# Arquivo que define os modelos de entrada e saída dos itens dos pedidos


class ItemPedidoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_pedido: str = Field(..., min_length=1, max_length=32)
    id_item: int = Field(..., ge=1)
    id_produto: str = Field(..., min_length=1, max_length=32)
    id_vendedor: str = Field(..., min_length=1, max_length=32)
    preco_BRL: float = Field(..., ge=0)
    preco_frete: float = Field(..., ge=0)


class ItemPedidoCreate(ItemPedidoBase):
    pass


class ItemPedidoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_produto: str | None = Field(None, min_length=1, max_length=32)
    id_vendedor: str | None = Field(None, min_length=1, max_length=32)
    preco_BRL: float | None = Field(None, ge=0)
    preco_frete: float | None = Field(None, ge=0)


class ItemPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_pedido: str
    id_item: int
    id_produto: str
    id_vendedor: str
    preco_BRL: float
    preco_frete: float