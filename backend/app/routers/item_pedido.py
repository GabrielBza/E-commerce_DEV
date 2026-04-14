from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoResponse, ItemPedidoUpdate
from app.services import item_pedido as item_pedido_service

router = APIRouter(prefix="/itens-pedidos", tags=["Itens dos Pedidos"])


# Arquivo que define as rotas relacionadas aos itens dos pedidos


@router.get("", response_model=list[ItemPedidoResponse])
def listar_itens_pedidos(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return item_pedido_service.listar_itens_pedidos(db, limit=limit, offset=offset)


@router.get("/pedido/{id_pedido}", response_model=list[ItemPedidoResponse])
def listar_itens_por_pedido(
    id_pedido: str,
    db: Session = Depends(get_db),
):
    return item_pedido_service.listar_itens_por_pedido(db, id_pedido)


@router.get("/{id_pedido}/{id_item}", response_model=ItemPedidoResponse)
def buscar_item_pedido_por_chave(
    id_pedido: str,
    id_item: int,
    db: Session = Depends(get_db),
):
    return item_pedido_service.buscar_item_pedido_por_chave(db, id_pedido, id_item)


@router.post("", response_model=ItemPedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_item_pedido(
    item_data: ItemPedidoCreate,
    db: Session = Depends(get_db),
):
    return item_pedido_service.criar_item_pedido(db, item_data)


@router.put("/{id_pedido}/{id_item}", response_model=ItemPedidoResponse)
def atualizar_item_pedido(
    id_pedido: str,
    id_item: int,
    item_data: ItemPedidoUpdate,
    db: Session = Depends(get_db),
):
    return item_pedido_service.atualizar_item_pedido(db, id_pedido, id_item, item_data)


@router.delete("/{id_pedido}/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item_pedido(
    id_pedido: str,
    id_item: int,
    db: Session = Depends(get_db),
):
    item_pedido_service.remover_item_pedido(db, id_pedido, id_item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)