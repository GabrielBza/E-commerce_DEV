from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.avaliacao_pedido import AvaliacaoPedido


# Arquivo responsável por realizar as operações de banco de dados relacionadas às avaliações de pedidos
# Consultas e operações de persistência


# Função para listar avaliações com paginação
def listar_avaliacoes_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[AvaliacaoPedido]:
    statement = (
        select(AvaliacaoPedido)
        .order_by(AvaliacaoPedido.data_comentario.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


# Função para buscar uma avaliação por id
def buscar_avaliacao_por_id(
    db: Session,
    id_avaliacao: str,
) -> Optional[AvaliacaoPedido]:
    statement = select(AvaliacaoPedido).where(AvaliacaoPedido.id_avaliacao == id_avaliacao)
    return db.scalar(statement)


# Função para listar avaliações de um pedido
def listar_avaliacoes_por_pedido(
    db: Session,
    id_pedido: str,
    limit: int = 50,
    offset: int = 0,
) -> list[AvaliacaoPedido]:
    statement = (
        select(AvaliacaoPedido)
        .where(AvaliacaoPedido.id_pedido == id_pedido)
        .order_by(AvaliacaoPedido.data_comentario.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


# Função auxiliar para verificar se já existe avaliação para o pedido
def buscar_avaliacao_por_pedido(
    db: Session,
    id_pedido: str,
) -> Optional[AvaliacaoPedido]:
    statement = select(AvaliacaoPedido).where(AvaliacaoPedido.id_pedido == id_pedido)
    return db.scalar(statement)


# Função para criar uma nova avaliação
def criar_avaliacao_pedido(
    db: Session,
    avaliacao_pedido: AvaliacaoPedido,
) -> AvaliacaoPedido:
    db.add(avaliacao_pedido)
    db.commit()
    db.refresh(avaliacao_pedido)
    return avaliacao_pedido


# Função para atualizar uma avaliação existente
def atualizar_avaliacao_pedido(
    db: Session,
    avaliacao_pedido: AvaliacaoPedido,
) -> AvaliacaoPedido:
    db.commit()
    db.refresh(avaliacao_pedido)
    return avaliacao_pedido


# Função para remover uma avaliação
def remover_avaliacao_pedido(
    db: Session,
    avaliacao_pedido: AvaliacaoPedido,
) -> None:
    db.delete(avaliacao_pedido)
    db.commit()