from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate,
    ProdutoDetalheResponse,
)
from app.services import produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Arquivo que define as rotas relacionadas aos produtos
# Recebe as requisições, extrai os dados necessários, chama as funções do serviço e retorna as respostas adequadas para cada endpoint

# Endpoint para listar produtos
@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return produto_service.listar_produtos(db, limit=limit, offset=offset)

# Endpoint para buscar produtos por um termo
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

# Endpoint para listar as categorias distintas dos produtos
@router.get("/categorias", response_model=list[str])
def listar_categorias_produtos(
    db: Session = Depends(get_db),
):
    return produto_service.listar_categorias_produtos(db)


# Endpoint para buscar um produto por id, onde é retornado o detalhe do produto, incluindo as métricas e avaliações
@router.get("/{id_produto}", response_model=ProdutoDetalheResponse)
def buscar_detalhe_produto(
    id_produto: str,
    db: Session = Depends(get_db),
):
    return produto_service.buscar_detalhe_produto(db, id_produto)


# Endpoint para criar um novo produto, onde é verificado se já existe um produto com as mesmas características
@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
):
    return produto_service.criar_produto(db, produto_data)


# Endpoint para atualizar um produto existente, onde é verificado se o produto existe e se as novas características não geram duplicidade
@router.put("/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(
    id_produto: str,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    return produto_service.atualizar_produto(db, id_produto, produto_data)


# Endpoint para remover um produto do banco de dados
@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    id_produto: str,
    db: Session = Depends(get_db),
):
    produto_service.remover_produto(db, id_produto)
    return Response(status_code=status.HTTP_204_NO_CONTENT)