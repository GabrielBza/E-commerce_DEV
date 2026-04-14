from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.vendedor import VendedorCreate, VendedorResponse, VendedorUpdate
from app.services import vendedor as vendedor_service

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


# Arquivo que define as rotas relacionadas aos vendedores


@router.get("", response_model=list[VendedorResponse])
def listar_vendedores(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return vendedor_service.listar_vendedores(db, limit=limit, offset=offset)


@router.get("/busca", response_model=list[VendedorResponse])
def buscar_vendedores_por_termo(
    termo: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return vendedor_service.buscar_vendedores_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


@router.get("/{id_vendedor}", response_model=VendedorResponse)
def buscar_vendedor_por_id(
    id_vendedor: str,
    db: Session = Depends(get_db),
):
    return vendedor_service.buscar_vendedor_por_id(db, id_vendedor)


@router.post("", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
def criar_vendedor(
    vendedor_data: VendedorCreate,
    db: Session = Depends(get_db),
):
    return vendedor_service.criar_vendedor(db, vendedor_data)


@router.put("/{id_vendedor}", response_model=VendedorResponse)
def atualizar_vendedor(
    id_vendedor: str,
    vendedor_data: VendedorUpdate,
    db: Session = Depends(get_db),
):
    return vendedor_service.atualizar_vendedor(db, id_vendedor, vendedor_data)


@router.delete("/{id_vendedor}", status_code=status.HTTP_204_NO_CONTENT)
def remover_vendedor(
    id_vendedor: str,
    db: Session = Depends(get_db),
):
    vendedor_service.remover_vendedor(db, id_vendedor)
    return Response(status_code=status.HTTP_204_NO_CONTENT)