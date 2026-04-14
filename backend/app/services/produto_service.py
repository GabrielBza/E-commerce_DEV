import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.repositories import produto_repository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def listar_produtos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Produto]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    return produto_repository.listar_produtos(db, limit=limit, offset=offset)


def buscar_produto_por_id(db: Session, id_produto: str) -> Produto:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    return produto


def buscar_produtos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Produto]:
    termo = termo.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    if not termo:
        return []

    return produto_repository.buscar_produtos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


def criar_produto(db: Session, produto_data: ProdutoCreate) -> Produto:
    produto_duplicado = produto_repository.buscar_produto_duplicado(
        db=db,
        nome_produto=produto_data.nome_produto,
        categoria_produto=produto_data.categoria_produto,
        peso_produto_gramas=produto_data.peso_produto_gramas,
        comprimento_centimetros=produto_data.comprimento_centimetros,
        altura_centimetros=produto_data.altura_centimetros,
        largura_centimetros=produto_data.largura_centimetros,
    )

    if produto_duplicado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um produto com as mesmas características.",
        )

    produto = Produto(
        id_produto=uuid.uuid4().hex,
        nome_produto=produto_data.nome_produto,
        categoria_produto=produto_data.categoria_produto,
        peso_produto_gramas=produto_data.peso_produto_gramas,
        comprimento_centimetros=produto_data.comprimento_centimetros,
        altura_centimetros=produto_data.altura_centimetros,
        largura_centimetros=produto_data.largura_centimetros,
    )

    return produto_repository.criar_produto(db, produto)


def atualizar_produto(
    db: Session,
    id_produto: str,
    produto_data: ProdutoUpdate,
) -> Produto:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    dados_atualizacao = produto_data.model_dump(exclude_unset=True)

    nome_produto = dados_atualizacao.get("nome_produto", produto.nome_produto)
    categoria_produto = dados_atualizacao.get("categoria_produto", produto.categoria_produto)
    peso_produto_gramas = dados_atualizacao.get("peso_produto_gramas", produto.peso_produto_gramas)
    comprimento_centimetros = dados_atualizacao.get("comprimento_centimetros", produto.comprimento_centimetros)
    altura_centimetros = dados_atualizacao.get("altura_centimetros", produto.altura_centimetros)
    largura_centimetros = dados_atualizacao.get("largura_centimetros", produto.largura_centimetros)

    produto_duplicado = produto_repository.buscar_produto_duplicado(
        db=db,
        nome_produto=nome_produto,
        categoria_produto=categoria_produto,
        peso_produto_gramas=peso_produto_gramas,
        comprimento_centimetros=comprimento_centimetros,
        altura_centimetros=altura_centimetros,
        largura_centimetros=largura_centimetros,
    )

    if produto_duplicado is not None and produto_duplicado.id_produto != produto.id_produto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe outro produto com as mesmas características.",
        )

    for campo, valor in dados_atualizacao.items():
        setattr(produto, campo, valor)

    return produto_repository.atualizar_produto(db, produto)


def remover_produto(db: Session, id_produto: str) -> None:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    produto_repository.remover_produto(db, produto)