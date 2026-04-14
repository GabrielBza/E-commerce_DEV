from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.produto import Produto


def listar_produtos(db: Session, limit: int = 50, offset: int = 0) -> list[Produto]:
    statement = (
        select(Produto)
        .order_by(Produto.nome_produto.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_produto_por_id(db: Session, id_produto: str) -> Optional[Produto]:
    statement = select(Produto).where(Produto.id_produto == id_produto)
    return db.scalar(statement)


def buscar_produtos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Produto]:
    termo = termo.strip()

    if not termo:
        return []

    statement = (
        select(Produto)
        .where(
            or_(
                Produto.nome_produto.ilike(f"%{termo}%"),
                Produto.categoria_produto.ilike(f"%{termo}%"),
            )
        )
        .order_by(Produto.nome_produto.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


def buscar_produto_duplicado(
    db: Session,
    nome_produto: str,
    categoria_produto: str,
    peso_produto_gramas: float | None,
    comprimento_centimetros: float | None,
    altura_centimetros: float | None,
    largura_centimetros: float | None,
) -> Optional[Produto]:
    statement = select(Produto).where(
        Produto.nome_produto == nome_produto,
        Produto.categoria_produto == categoria_produto,
        Produto.peso_produto_gramas == peso_produto_gramas,
        Produto.comprimento_centimetros == comprimento_centimetros,
        Produto.altura_centimetros == altura_centimetros,
        Produto.largura_centimetros == largura_centimetros,
    )
    return db.scalar(statement)


def criar_produto(db: Session, produto: Produto) -> Produto:
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def atualizar_produto(db: Session, produto: Produto) -> Produto:
    db.commit()
    db.refresh(produto)
    return produto


def remover_produto(db: Session, produto: Produto) -> None:
    db.delete(produto)
    db.commit()