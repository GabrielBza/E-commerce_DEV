from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.consumidor import Consumidor


# Arquivo responsável por realizar as operações de banco de dados relacionadas aos consumidores


def listar_consumidores(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Consumidor]:
    statement = (
        select(Consumidor)
        .order_by(Consumidor.nome_consumidor.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_consumidor_por_id(
    db: Session,
    id_consumidor: str,
) -> Optional[Consumidor]:
    statement = select(Consumidor).where(Consumidor.id_consumidor == id_consumidor)
    return db.scalar(statement)


def buscar_consumidores_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Consumidor]:
    termo = termo.strip()

    if not termo:
        return []

    statement = (
        select(Consumidor)
        .where(
            or_(
                Consumidor.nome_consumidor.ilike(f"%{termo}%"),
                Consumidor.cidade.ilike(f"%{termo}%"),
                Consumidor.estado.ilike(f"%{termo}%"),
                Consumidor.prefixo_cep.ilike(f"%{termo}%"),
            )
        )
        .order_by(Consumidor.nome_consumidor.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_consumidor_duplicado(
    db: Session,
    prefixo_cep: str,
    nome_consumidor: str,
    cidade: str,
    estado: str,
) -> Optional[Consumidor]:
    statement = select(Consumidor).where(
        Consumidor.prefixo_cep == prefixo_cep,
        Consumidor.nome_consumidor == nome_consumidor,
        Consumidor.cidade == cidade,
        Consumidor.estado == estado,
    )
    return db.scalar(statement)


def criar_consumidor(
    db: Session,
    consumidor: Consumidor,
) -> Consumidor:
    db.add(consumidor)
    db.commit()
    db.refresh(consumidor)
    return consumidor


def atualizar_consumidor(
    db: Session,
    consumidor: Consumidor,
) -> Consumidor:
    db.commit()
    db.refresh(consumidor)
    return consumidor


def remover_consumidor(
    db: Session,
    consumidor: Consumidor,
) -> None:
    db.delete(consumidor)
    db.commit()