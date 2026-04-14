from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.vendedor import Vendedor


# Arquivo responsável por realizar as operações de banco de dados relacionadas aos vendedores


def listar_vendedores(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Vendedor]:
    statement = (
        select(Vendedor)
        .order_by(Vendedor.nome_vendedor.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_vendedor_por_id(
    db: Session,
    id_vendedor: str,
) -> Optional[Vendedor]:
    statement = select(Vendedor).where(Vendedor.id_vendedor == id_vendedor)
    return db.scalar(statement)


def buscar_vendedores_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Vendedor]:
    termo = termo.strip()

    if not termo:
        return []

    statement = (
        select(Vendedor)
        .where(
            or_(
                Vendedor.nome_vendedor.ilike(f"%{termo}%"),
                Vendedor.cidade.ilike(f"%{termo}%"),
                Vendedor.estado.ilike(f"%{termo}%"),
                Vendedor.prefixo_cep.ilike(f"%{termo}%"),
            )
        )
        .order_by(Vendedor.nome_vendedor.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_vendedor_duplicado(
    db: Session,
    nome_vendedor: str,
    prefixo_cep: str,
    cidade: str,
    estado: str,
) -> Optional[Vendedor]:
    statement = select(Vendedor).where(
        Vendedor.nome_vendedor == nome_vendedor,
        Vendedor.prefixo_cep == prefixo_cep,
        Vendedor.cidade == cidade,
        Vendedor.estado == estado,
    )
    return db.scalar(statement)


def criar_vendedor(
    db: Session,
    vendedor: Vendedor,
) -> Vendedor:
    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)
    return vendedor


def atualizar_vendedor(
    db: Session,
    vendedor: Vendedor,
) -> Vendedor:
    db.commit()
    db.refresh(vendedor)
    return vendedor


def remover_vendedor(
    db: Session,
    vendedor: Vendedor,
) -> None:
    db.delete(vendedor)
    db.commit()