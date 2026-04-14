from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item_pedido import ItemPedido
from app.repositories import item_pedido as item_pedido_repository
from app.repositories import pedido as pedido_repository
from app.repositories import produto as produto_repository
from app.repositories import vendedor as vendedor_repository
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoResponse, ItemPedidoUpdate


# Arquivo para gerenciar a lógica de negócio relacionada aos itens dos pedidos


def listar_itens_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[ItemPedidoResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    itens = item_pedido_repository.listar_itens_pedidos(db, limit=limit, offset=offset)
    return [ItemPedidoResponse.model_validate(item) for item in itens]


def buscar_item_pedido_por_chave(
    db: Session,
    id_pedido: str,
    id_item: int,
) -> ItemPedidoResponse:
    id_pedido = id_pedido.strip()

    item = item_pedido_repository.buscar_item_pedido_por_chave(db, id_pedido, id_item)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    return ItemPedidoResponse.model_validate(item)


def listar_itens_por_pedido(
    db: Session,
    id_pedido: str,
) -> list[ItemPedidoResponse]:
    id_pedido = id_pedido.strip()

    pedido = pedido_repository.buscar_pedido_por_id(db, id_pedido)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    itens = item_pedido_repository.listar_itens_por_pedido(db, id_pedido)
    return [ItemPedidoResponse.model_validate(item) for item in itens]


def criar_item_pedido(
    db: Session,
    item_data: ItemPedidoCreate,
) -> ItemPedidoResponse:
    pedido = pedido_repository.buscar_pedido_por_id(db, item_data.id_pedido)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    produto = produto_repository.buscar_produto_por_id(db, item_data.id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    vendedor = vendedor_repository.buscar_vendedor_por_id(db, item_data.id_vendedor)
    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado.",
        )

    item_duplicado = item_pedido_repository.buscar_item_duplicado(
        db,
        id_pedido=item_data.id_pedido,
        id_item=item_data.id_item,
    )

    if item_duplicado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um item com esta chave composta no pedido.",
        )

    item = ItemPedido(
        id_pedido=item_data.id_pedido,
        id_item=item_data.id_item,
        id_produto=item_data.id_produto,
        id_vendedor=item_data.id_vendedor,
        preco_BRL=item_data.preco_BRL,
        preco_frete=item_data.preco_frete,
    )

    item_criado = item_pedido_repository.criar_item_pedido(db, item)
    return ItemPedidoResponse.model_validate(item_criado)


def atualizar_item_pedido(
    db: Session,
    id_pedido: str,
    id_item: int,
    item_data: ItemPedidoUpdate,
) -> ItemPedidoResponse:
    id_pedido = id_pedido.strip()

    item = item_pedido_repository.buscar_item_pedido_por_chave(db, id_pedido, id_item)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    dados_atualizacao = item_data.model_dump(exclude_unset=True)

    novo_id_produto = dados_atualizacao.get("id_produto", item.id_produto)
    novo_id_vendedor = dados_atualizacao.get("id_vendedor", item.id_vendedor)

    produto = produto_repository.buscar_produto_por_id(db, novo_id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    vendedor = vendedor_repository.buscar_vendedor_por_id(db, novo_id_vendedor)
    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado.",
        )

    for campo, valor in dados_atualizacao.items():
        setattr(item, campo, valor)

    item_atualizado = item_pedido_repository.atualizar_item_pedido(db, item)
    return ItemPedidoResponse.model_validate(item_atualizado)


def remover_item_pedido(
    db: Session,
    id_pedido: str,
    id_item: int,
) -> None:
    id_pedido = id_pedido.strip()

    item = item_pedido_repository.buscar_item_pedido_por_chave(db, id_pedido, id_item)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item do pedido não encontrado.",
        )

    item_pedido_repository.remover_item_pedido(db, item)