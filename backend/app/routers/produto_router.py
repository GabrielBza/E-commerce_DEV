from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services import produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return produto_service.listar_produtos(db, limit=limit, offset=offset)


@router.get("/busca", response_model=list[ProdutoResponse])
def buscar_produtos_por_termo(
    termo: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return produto_service.buscar_produtos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


@router.get("/{id_produto}", response_model=ProdutoResponse)
def buscar_produto_por_id(
    id_produto: str,
    db: Session = Depends(get_db),
):
    return produto_service.buscar_produto_por_id(db, id_produto)


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
):
    return produto_service.criar_produto(db, produto_data)


@router.put("/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(
    id_produto: str,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    return produto_service.atualizar_produto(db, id_produto, produto_data)


@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    id_produto: str,
    db: Session = Depends(get_db),
):
    produto_service.remover_produto(db, id_produto)
    return Response(status_code=status.HTTP_204_NO_CONTENT)