import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.repositories import produto_repository
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
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
) -> list[ProdutoResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    produtos = produto_repository.listar_produtos(db, limit=limit, offset=offset)

    return [montar_produto_response(db, produto) for produto in produtos]


# Função para buscar um produto por id
def buscar_produto_por_id(db: Session, id_produto: str) -> ProdutoResponse:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Retorno de um 404 caso o produto não seja encontrado
            detail="Produto não encontrado.",
        )

    return montar_produto_response(db, produto)


# Função para buscar o detalhe de um produto, onde além dos dados do produto, são retornados os dados relacionados às métricas e avaliações do produto
def buscar_detalhe_produto(db: Session, id_produto: str) -> ProdutoDetalheResponse:
    id_produto = id_produto.strip()

    produto = produto_repository.buscar_produto_por_id(db, id_produto)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        ) # Retorno de um 404 caso o produto não seja encontrado

    imagem_categoria = produto_repository.buscar_imagem_por_categoria(
        db,
        produto.categoria_produto,
    )

    metricas = produto_repository.buscar_metricas_detalhe_produto(db, id_produto) # Busca as métricas relacionadas ao produto para incluir na resposta
    avaliacoes = produto_repository.buscar_avaliacoes_produto(db, id_produto) # Busca as avaliações do produto para incluir na resposta

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
        imagem_categoria=imagem_categoria,
    )


# Função para buscar produtos por um termo inserido pelo user (Esse termo é buscado no nome e na categoria)
def buscar_produtos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[ProdutoResponse]:
    termo = termo.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    if not termo:
        return [] # Retorno de uma lista vazia caso o termo seja vazio ou apenas espaços em branco

    produtos = produto_repository.buscar_produtos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )

    return [montar_produto_response(db, produto) for produto in produtos]


# Função para criar um novo produto, onde é verificado se já existe um produto com as mesmas características para evitar duplicidade
def criar_produto(db: Session, produto_data: ProdutoCreate) -> ProdutoResponse:
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
        ) # Retorno de um 409 caso já exista um produto com as mesmas características

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

    produto_criado = produto_repository.criar_produto(db, produto)
    return montar_produto_response(db, produto_criado)


# Função para atualizar um produto existente, onde é verificado se o produto existe e se as novas características não geram duplicidade com outro produto
def atualizar_produto(
    db: Session,
    id_produto: str,
    produto_data: ProdutoUpdate,
) -> ProdutoResponse:
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

    produto_atualizado = produto_repository.atualizar_produto(db, produto)
    return montar_produto_response(db, produto_atualizado)


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


def montar_produto_response(db: Session, produto: Produto) -> ProdutoResponse:
    imagem_categoria = produto_repository.buscar_imagem_por_categoria(
        db,
        produto.categoria_produto,
    )

    return ProdutoResponse(
        id_produto=produto.id_produto,
        nome_produto=produto.nome_produto,
        categoria_produto=produto.categoria_produto,
        peso_produto_gramas=produto.peso_produto_gramas,
        comprimento_centimetros=produto.comprimento_centimetros,
        altura_centimetros=produto.altura_centimetros,
        largura_centimetros=produto.largura_centimetros,
        imagem_categoria=imagem_categoria,
    )

# Função para listar as categorias distintas dos produtos
def listar_categorias_produtos(db: Session) -> list[str]:
    return produto_repository.listar_categorias_produtos(db)