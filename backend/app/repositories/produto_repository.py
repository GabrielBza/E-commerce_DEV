from typing import Optional

from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.categoria_imagem import CategoriaImagem

# Arquivo responsável por realizar as operações de banco de dados relacionadas aos produtos
# Colsultas e operações de persistência


# Função para listar produtos com paginação (limit e offset), ordenando por nome
def listar_produtos(db: Session, limit: int = 50, offset: int = 0) -> list[Produto]:
    statement = (
        select(Produto)
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())


# Função para buscar um produto por id, retornando None caso não seja encontrado
def buscar_produto_por_id(db: Session, id_produto: str) -> Optional[Produto]:
    statement = select(Produto).where(Produto.id_produto == id_produto)
    return db.scalar(statement)


# Função para buscar produtos por um termo inserido pelo user (Esse termo é buscado no nome e na categoria)
def buscar_produtos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Produto]:
    termo = termo.strip()

    if not termo:
        return []

    statement = (
        select(Produto)
        .where(
            or_(
                Produto.nome_produto.ilike(f"%{termo}%"),
                Produto.categoria_produto.ilike(f"%{termo}%"),
            )
        )
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement).all())

# Função auxiliar para buscar um produto com os mesmos campos (exceto id) para evitar duplicidade de produtos
def buscar_produto_duplicado(
    db: Session,
    nome_produto: str,
    categoria_produto: str,
    peso_produto_gramas: float | None,
    comprimento_centimetros: float | None,
    altura_centimetros: float | None,
    largura_centimetros: float | None,
) -> Optional[Produto]:
    statement = select(Produto).where(
        Produto.nome_produto == nome_produto,
        Produto.categoria_produto == categoria_produto,
        Produto.peso_produto_gramas == peso_produto_gramas,
        Produto.comprimento_centimetros == comprimento_centimetros,
        Produto.altura_centimetros == altura_centimetros,
        Produto.largura_centimetros == largura_centimetros,
    )
    return db.scalar(statement)

# Função para buscar o produto e suas métricas detalhadas (quantidade de vendas, valor total vendido, quantidade de avaliações e média das avaliações)
def buscar_metricas_detalhe_produto(db: Session, id_produto: str) -> dict:
    quantidade_vendas_stmt = (
        select(
            func.count(ItemPedido.id_item).label("quantidade_vendas"),
            func.coalesce(func.sum(ItemPedido.preco_BRL), 0.0).label("valor_total_vendido"),
        )
        .where(ItemPedido.id_produto == id_produto)
    ) # Querry que busca a quantidade de vendas e o valor total vendido do produto

    resultado_vendas = db.execute(quantidade_vendas_stmt).one()

    pedidos_subquery = (
        select(ItemPedido.id_pedido)
        .where(ItemPedido.id_produto == id_produto)
        .distinct()
        .subquery()
    ) # Querry que busca os pedidos relacionados ao produto

    quantidade_avaliacoes_stmt = (
        select(
            func.count(AvaliacaoPedido.id_avaliacao).label("quantidade_avaliacoes"),
            func.avg(AvaliacaoPedido.avaliacao).label("media_avaliacoes"),
        )
        .where(AvaliacaoPedido.id_pedido.in_(select(pedidos_subquery.c.id_pedido)))
    ) # Querry que busca a quantidade de avaliações e a média das avaliações do produto

    resultado_avaliacoes = db.execute(quantidade_avaliacoes_stmt).one()

    return {
        "quantidade_vendas": int(resultado_vendas.quantidade_vendas or 0),
        "valor_total_vendido": float(resultado_vendas.valor_total_vendido or 0.0),
        "quantidade_avaliacoes": int(resultado_avaliacoes.quantidade_avaliacoes or 0),
        "media_avaliacoes": float(resultado_avaliacoes.media_avaliacoes)
        if resultado_avaliacoes.media_avaliacoes is not None
        else None,
    }

# Função para buscar as avaliações do produto, retornando uma lista das avaliações mais recentes relacionadas ao produto
def buscar_avaliacoes_produto(
    db: Session,
    id_produto: str,
    limit: int = 5,
) -> list[AvaliacaoPedido]:
    pedidos_subquery = (
        select(ItemPedido.id_pedido)
        .where(ItemPedido.id_produto == id_produto)
        .distinct()
        .subquery()
    ) # Querry que busca os pedidos relacionados ao produto

    statement = (
        select(AvaliacaoPedido)
        .where(AvaliacaoPedido.id_pedido.in_(select(pedidos_subquery.c.id_pedido)))
        .order_by(AvaliacaoPedido.data_comentario.desc())
        .limit(limit)
    ) # Querry que busca as avaliações relacionadas aos pedidos do produto

    # Função quebrada nessas 2 querries para evitar joins grandes e ganhar desempenho

    return list(db.scalars(statement).all())


# Função para criar um novo produto no banco de dados
def criar_produto(db: Session, produto: Produto) -> Produto:
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


# Função para atualizar um produto existente no banco de dados
def atualizar_produto(db: Session, produto: Produto) -> Produto:
    db.commit()
    db.refresh(produto)
    return produto


# Função para remover um produto do banco de dados
def remover_produto(db: Session, produto: Produto) -> None:
    db.delete(produto)
    db.commit()

# Função auxiliar para buscar a imagem relacionada à categoria do produto
def buscar_imagem_por_categoria(db: Session, categoria: str) -> Optional[str]:
    statement = (
        select(CategoriaImagem.link)
        .where(CategoriaImagem.categoria == categoria)
    )
    return db.scalar(statement)

# Função para listar as categorias distintas dos produtos
def listar_categorias_produtos(db: Session) -> list[str]:
    statement = (
        select(Produto.categoria_produto)
        .distinct()
        .order_by(Produto.categoria_produto.asc())
    )
    return list(db.scalars(statement).all())