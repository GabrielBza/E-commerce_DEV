import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.repositories import produto_repository
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoDetalheResponse,
    AvaliacaoProdutoResponse,
)

# Arquivo para gerenciar a lógica de negócio relacionada aos produtos
# Realiza validações, verificações e aplicação das regras de negócio
# Faz o intemédio entre o router e o repository preparando os dados para serem persistidos ou retornados


# Função para listar produtos com paginação (limit e offset)
def listar_produtos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Produto]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    return produto_repository.listar_produtos(db, limit=limit, offset=offset)


# Função para buscar um produto por id
def buscar_produto_por_id(db: Session, id_produto: str) -> Produto:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        ) # Retorno de um 404 caso o produto não seja encontrado

    return produto


# Função para buscar o detalhe de um produto, onde além dos dados do produto, são retornados os dados relacionados às métricas e avaliações do produto
def buscar_detalhe_produto(db: Session, id_produto: str) -> ProdutoDetalheResponse:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        ) # Retorno de um 404 caso o produto não seja encontrado

    metricas = produto_repository.buscar_metricas_detalhe_produto(db, id_produto) # Busca das métricas relacionadas ao produto
    avaliacoes = produto_repository.buscar_avaliacoes_produto(db, id_produto) # Busca das avaliações relacionadas ao produto

    avaliacoes_response = [
        AvaliacaoProdutoResponse(
            id_avaliacao=avaliacao.id_avaliacao,
            id_pedido=avaliacao.id_pedido,
            avaliacao=avaliacao.avaliacao,
            titulo_comentario=avaliacao.titulo_comentario,
            comentario=avaliacao.comentario,
            data_comentario=avaliacao.data_comentario.isoformat() if avaliacao.data_comentario else None,
            data_resposta=avaliacao.data_resposta.isoformat() if avaliacao.data_resposta else None,
        )
        for avaliacao in avaliacoes
    ]

    return ProdutoDetalheResponse(
        id_produto=produto.id_produto,
        nome_produto=produto.nome_produto,
        categoria_produto=produto.categoria_produto,
        peso_produto_gramas=produto.peso_produto_gramas,
        comprimento_centimetros=produto.comprimento_centimetros,
        altura_centimetros=produto.altura_centimetros,
        largura_centimetros=produto.largura_centimetros,
        quantidade_vendas=metricas["quantidade_vendas"],
        valor_total_vendido=metricas["valor_total_vendido"],
        quantidade_avaliacoes=metricas["quantidade_avaliacoes"],
        media_avaliacoes=metricas["media_avaliacoes"],
        avaliacoes=avaliacoes_response,
    )


# Função para buscar produtos por um termo inserido pelo user (Esse termo é buscado no nome e na categoria)
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
        return [] # Retorno de uma lista vazia caso o termo seja vazio ou apenas espaços em branco

    return produto_repository.buscar_produtos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


# Função para criar um novo produto, onde é verificado se já existe um produto com as mesmas características para evitar duplicidade
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
        ) # Retorno de um 409 caso já exista um produto com as mesmas características para evitar duplicidade

    produto = Produto(
        # Geração do ID do produto usando UUID4 para seguir o mesmo padrão dos dados já existente e praticamente evita conflitos por ter um range gigantesco de possibilidades
        id_produto=uuid.uuid4().hex,
        nome_produto=produto_data.nome_produto,
        categoria_produto=produto_data.categoria_produto,
        peso_produto_gramas=produto_data.peso_produto_gramas,
        comprimento_centimetros=produto_data.comprimento_centimetros,
        altura_centimetros=produto_data.altura_centimetros,
        largura_centimetros=produto_data.largura_centimetros,
    )

    return produto_repository.criar_produto(db, produto)


# Função para atualizar um produto existente, onde é verificado se o produto existe e se as novas características não geram duplicidade com outro produto
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


# Função para remover um produto do banco de dados
def remover_produto(db: Session, id_produto: str) -> None:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    produto_repository.remover_produto(db, produto)