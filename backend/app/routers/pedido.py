from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate
from app.services import pedido as pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# Arquivo que define as rotas relacionadas aos pedidos


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return pedido_service.listar_pedidos(db, limit=limit, offset=offset)


@router.get("/busca", response_model=list[PedidoResponse])
def buscar_pedidos_por_termo(
    termo: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return pedido_service.buscar_pedidos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


@router.get("/consumidor/{id_consumidor}", response_model=list[PedidoResponse])
def listar_pedidos_por_consumidor(
    id_consumidor: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return pedido_service.listar_pedidos_por_consumidor(
        db,
        id_consumidor=id_consumidor,
        limit=limit,
        offset=offset,
    )


@router.get("/{id_pedido}", response_model=PedidoResponse)
def buscar_pedido_por_id(
    id_pedido: str,
    db: Session = Depends(get_db),
):
    return pedido_service.buscar_pedido_por_id(db, id_pedido)


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db),
):
    return pedido_service.criar_pedido(db, pedido_data)


@router.put("/{id_pedido}", response_model=PedidoResponse)
def atualizar_pedido(
    id_pedido: str,
    pedido_data: PedidoUpdate,
    db: Session = Depends(get_db),
):
    return pedido_service.atualizar_pedido(db, id_pedido, pedido_data)


@router.delete("/{id_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pedido(
    id_pedido: str,
    db: Session = Depends(get_db),
):
    pedido_service.remover_pedido(db, id_pedido)
    return Response(status_code=status.HTTP_204_NO_CONTENT)