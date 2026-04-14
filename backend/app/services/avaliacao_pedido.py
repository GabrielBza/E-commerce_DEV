import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.avaliacao_pedido import AvaliacaoPedido
from app.repositories import avaliacao_pedido as avaliacao_pedido_repository
from app.repositories import pedido as pedido_repository
from app.schemas.avaliacao_pedido import (
    AvaliacaoPedidoCreate,
    AvaliacaoPedidoResponse,
    AvaliacaoPedidoUpdate,
)


# Arquivo para gerenciar a lógica de negócio relacionada às avaliações de pedidos
# Realiza validações, verificações e aplicação das regras de negócio


def listar_avaliacoes_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[AvaliacaoPedidoResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    avaliacoes = avaliacao_pedido_repository.listar_avaliacoes_pedidos(
        db,
        limit=limit,
        offset=offset,
    )
    return [AvaliacaoPedidoResponse.model_validate(avaliacao) for avaliacao in avaliacoes]


def buscar_avaliacao_por_id(
    db: Session,
    id_avaliacao: str,
) -> AvaliacaoPedidoResponse:
    id_avaliacao = id_avaliacao.strip()

    avaliacao = avaliacao_pedido_repository.buscar_avaliacao_por_id(db, id_avaliacao)

    if avaliacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação do pedido não encontrada.",
        )

    return AvaliacaoPedidoResponse.model_validate(avaliacao)


def listar_avaliacoes_por_pedido(
    db: Session,
    id_pedido: str,
    limit: int = 50,
    offset: int = 0,
) -> list[AvaliacaoPedidoResponse]:
    id_pedido = id_pedido.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    pedido = pedido_repository.buscar_pedido_por_id(db, id_pedido)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    avaliacoes = avaliacao_pedido_repository.listar_avaliacoes_por_pedido(
        db,
        id_pedido=id_pedido,
        limit=limit,
        offset=offset,
    )

    return [AvaliacaoPedidoResponse.model_validate(avaliacao) for avaliacao in avaliacoes]


def criar_avaliacao_pedido(
    db: Session,
    avaliacao_data: AvaliacaoPedidoCreate,
) -> AvaliacaoPedidoResponse:
    pedido = pedido_repository.buscar_pedido_por_id(db, avaliacao_data.id_pedido)

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    avaliacao_existente = avaliacao_pedido_repository.buscar_avaliacao_por_pedido(
        db,
        avaliacao_data.id_pedido,
    )

    if avaliacao_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma avaliação cadastrada para este pedido.",
        )

    avaliacao = AvaliacaoPedido(
        id_avaliacao=uuid.uuid4().hex,
        id_pedido=avaliacao_data.id_pedido,
        avaliacao=avaliacao_data.avaliacao,
        titulo_comentario=avaliacao_data.titulo_comentario,
        comentario=avaliacao_data.comentario,
        data_comentario=avaliacao_data.data_comentario,
        data_resposta=avaliacao_data.data_resposta,
    )

    avaliacao_criada = avaliacao_pedido_repository.criar_avaliacao_pedido(db, avaliacao)
    return AvaliacaoPedidoResponse.model_validate(avaliacao_criada)


def atualizar_avaliacao_pedido(
    db: Session,
    id_avaliacao: str,
    avaliacao_data: AvaliacaoPedidoUpdate,
) -> AvaliacaoPedidoResponse:
    id_avaliacao = id_avaliacao.strip()

    avaliacao = avaliacao_pedido_repository.buscar_avaliacao_por_id(db, id_avaliacao)

    if avaliacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação do pedido não encontrada.",
        )

    dados_atualizacao = avaliacao_data.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(avaliacao, campo, valor)

    avaliacao_atualizada = avaliacao_pedido_repository.atualizar_avaliacao_pedido(db, avaliacao)
    return AvaliacaoPedidoResponse.model_validate(avaliacao_atualizada)


def remover_avaliacao_pedido(
    db: Session,
    id_avaliacao: str,
) -> None:
    id_avaliacao = id_avaliacao.strip()

    avaliacao = avaliacao_pedido_repository.buscar_avaliacao_por_id(db, id_avaliacao)

    if avaliacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação do pedido não encontrada.",
        )

    avaliacao_pedido_repository.remover_avaliacao_pedido(db, avaliacao)