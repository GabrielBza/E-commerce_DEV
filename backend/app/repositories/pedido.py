from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.pedido import Pedido


# Arquivo responsável por realizar as operações de banco de dados relacionadas aos pedidos


def listar_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Pedido]:
    statement = (
        select(Pedido)
        .order_by(Pedido.pedido_compra_timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_pedido_por_id(
    db: Session,
    id_pedido: str,
) -> Optional[Pedido]:
    statement = select(Pedido).where(Pedido.id_pedido == id_pedido)
    return db.scalar(statement)


def buscar_pedidos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Pedido]:
    termo = termo.strip()

    if not termo:
        return []

    statement = (
        select(Pedido)
        .where(
            or_(
                Pedido.status.ilike(f"%{termo}%"),
                Pedido.id_consumidor.ilike(f"%{termo}%"),
                Pedido.entrega_no_prazo.ilike(f"%{termo}%"),
            )
        )
        .order_by(Pedido.pedido_compra_timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def listar_pedidos_por_consumidor(
    db: Session,
    id_consumidor: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Pedido]:
    statement = (
        select(Pedido)
        .where(Pedido.id_consumidor == id_consumidor)
        .order_by(Pedido.pedido_compra_timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_pedido_duplicado(
    db: Session,
    id_consumidor: str,
    status: str,
    pedido_compra_timestamp,
) -> Optional[Pedido]:
    statement = select(Pedido).where(
        Pedido.id_consumidor == id_consumidor,
        Pedido.status == status,
        Pedido.pedido_compra_timestamp == pedido_compra_timestamp,
    )
    return db.scalar(statement)


def criar_pedido(
    db: Session,
    pedido: Pedido,
) -> Pedido:
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def atualizar_pedido(
    db: Session,
    pedido: Pedido,
) -> Pedido:
    db.commit()
    db.refresh(pedido)
    return pedido


def remover_pedido(
    db: Session,
    pedido: Pedido,
) -> None:
    db.delete(pedido)
    db.commit()