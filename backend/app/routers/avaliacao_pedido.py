from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.avaliacao_pedido import (
    AvaliacaoPedidoCreate,
    AvaliacaoPedidoResponse,
    AvaliacaoPedidoUpdate,
)
from app.services import avaliacao_pedido as avaliacao_pedido_service

router = APIRouter(prefix="/avaliacoes-pedidos", tags=["Avaliações de Pedidos"])


# Arquivo que define as rotas relacionadas às avaliações de pedidos


@router.get("", response_model=list[AvaliacaoPedidoResponse])
def listar_avaliacoes_pedidos(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return avaliacao_pedido_service.listar_avaliacoes_pedidos(db, limit=limit, offset=offset)


@router.get("/pedido/{id_pedido}", response_model=list[AvaliacaoPedidoResponse])
def listar_avaliacoes_por_pedido(
    id_pedido: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return avaliacao_pedido_service.listar_avaliacoes_por_pedido(
        db,
        id_pedido=id_pedido,
        limit=limit,
        offset=offset,
    )


@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoResponse)
def buscar_avaliacao_por_id(
    id_avaliacao: str,
    db: Session = Depends(get_db),
):
    return avaliacao_pedido_service.buscar_avaliacao_por_id(db, id_avaliacao)


@router.post("", response_model=AvaliacaoPedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_avaliacao_pedido(
    avaliacao_data: AvaliacaoPedidoCreate,
    db: Session = Depends(get_db),
):
    return avaliacao_pedido_service.criar_avaliacao_pedido(db, avaliacao_data)


@router.put("/{id_avaliacao}", response_model=AvaliacaoPedidoResponse)
def atualizar_avaliacao_pedido(
    id_avaliacao: str,
    avaliacao_data: AvaliacaoPedidoUpdate,
    db: Session = Depends(get_db),
):
    return avaliacao_pedido_service.atualizar_avaliacao_pedido(
        db,
        id_avaliacao=id_avaliacao,
        avaliacao_data=avaliacao_data,
    )


@router.delete("/{id_avaliacao}", status_code=status.HTTP_204_NO_CONTENT)
def remover_avaliacao_pedido(
    id_avaliacao: str,
    db: Session = Depends(get_db),
):
    avaliacao_pedido_service.remover_avaliacao_pedido(db, id_avaliacao)
    return Response(status_code=status.HTTP_204_NO_CONTENT)