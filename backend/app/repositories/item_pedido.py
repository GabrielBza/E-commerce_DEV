from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item_pedido import ItemPedido


# Arquivo responsável por realizar as operações de banco de dados relacionadas aos itens dos pedidos


def listar_itens_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[ItemPedido]:
    statement = (
        select(ItemPedido)
        .order_by(ItemPedido.id_pedido.asc(), ItemPedido.id_item.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_item_pedido_por_chave(
    db: Session,
    id_pedido: str,
    id_item: int,
) -> Optional[ItemPedido]:
    statement = select(ItemPedido).where(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item,
    )
    return db.scalar(statement)


def listar_itens_por_pedido(
    db: Session,
    id_pedido: str,
) -> list[ItemPedido]:
    statement = (
        select(ItemPedido)
        .where(ItemPedido.id_pedido == id_pedido)
        .order_by(ItemPedido.id_item.asc())
    )
    return list(db.scalars(statement).all())


def buscar_item_duplicado(
    db: Session,
    id_pedido: str,
    id_item: int,
) -> Optional[ItemPedido]:
    statement = select(ItemPedido).where(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item,
    )
    return db.scalar(statement)


def criar_item_pedido(
    db: Session,
    item_pedido: ItemPedido,
) -> ItemPedido:
    db.add(item_pedido)
    db.commit()
    db.refresh(item_pedido)
    return item_pedido


def atualizar_item_pedido(
    db: Session,
    item_pedido: ItemPedido,
) -> ItemPedido:
    db.commit()
    db.refresh(item_pedido)
    return item_pedido


def remover_item_pedido(
    db: Session,
    item_pedido: ItemPedido,
) -> None:
    db.delete(item_pedido)
    db.commit()