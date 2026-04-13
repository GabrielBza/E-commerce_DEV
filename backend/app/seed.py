from pathlib import Path
from datetime import datetime
import csv

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.vendedor import Vendedor
from app.models.consumidor import Consumidor
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.categoria_imagem import CategoriaImagem


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def empty_to_none(value: str | None):
    if value is None:
        return None
    value = value.strip()
    return value if value != "" else None


def to_float(value: str | None):
    value = empty_to_none(value)
    return float(value) if value is not None else None


def to_int(value: str | None):
    value = empty_to_none(value)
    return int(value) if value is not None else None


def to_datetime(value: str | None):
    value = empty_to_none(value)
    if value is None:
        return None
    return datetime.fromisoformat(value)


def to_date(value: str | None):
    value = empty_to_none(value)
    if value is None:
        return None
    return datetime.fromisoformat(value).date()


def read_csv_rows(csv_path: Path):
    with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def seed_vendedores(db: Session):
    if db.query(Vendedor).first():
        print("Tabela vendedores já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "dim_vendedores.csv"
    rows = read_csv_rows(csv_path)

    vendedores = []
    for index, row in enumerate(rows):
        try:
            vendedor = Vendedor(
                id_vendedor=empty_to_none(row.get("id_vendedor")),
                nome_vendedor=empty_to_none(row.get("nome_vendedor")),
                prefixo_cep=empty_to_none(row.get("prefixo_cep")),
                cidade=empty_to_none(row.get("cidade")),
                estado=empty_to_none(row.get("estado")),
            )
            vendedores.append(vendedor)
        except Exception as e:
            print(f"Erro em vendedores na linha {index}: {row}")
            raise e

    db.add_all(vendedores)
    db.commit()
    print(f"{len(vendedores)} vendedores inseridos com sucesso.")


def seed_consumidores(db: Session):
    if db.query(Consumidor).first():
        print("Tabela consumidores já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "dim_consumidores.csv"
    rows = read_csv_rows(csv_path)

    consumidores = []
    for index, row in enumerate(rows):
        try:
            consumidor = Consumidor(
                id_consumidor=empty_to_none(row.get("id_consumidor")),
                prefixo_cep=empty_to_none(row.get("prefixo_cep")),
                nome_consumidor=empty_to_none(row.get("nome_consumidor")),
                cidade=empty_to_none(row.get("cidade")),
                estado=empty_to_none(row.get("estado")),
            )
            consumidores.append(consumidor)
        except Exception as e:
            print(f"Erro em consumidores na linha {index}: {row}")
            raise e

    db.add_all(consumidores)
    db.commit()
    print(f"{len(consumidores)} consumidores inseridos com sucesso.")


def seed_produtos(db: Session):
    if db.query(Produto).first():
        print("Tabela produtos já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "dim_produtos.csv"
    rows = read_csv_rows(csv_path)

    produtos = []

    for index, row in enumerate(rows):
        try:
            categoria = empty_to_none(row.get("categoria_produto"))

            if categoria is None:
                categoria = "sem_categoria"

            produto = Produto(
                id_produto=empty_to_none(row.get("id_produto")),
                nome_produto=empty_to_none(row.get("nome_produto")),
                categoria_produto=categoria,
                peso_produto_gramas=to_float(row.get("peso_produto_gramas")),
                comprimento_centimetros=to_float(row.get("comprimento_centimetros")),
                altura_centimetros=to_float(row.get("altura_centimetros")),
                largura_centimetros=to_float(row.get("largura_centimetros")),
            )
            produtos.append(produto)
        except Exception as e:
            print(f"Erro em produtos na linha {index}: {row}")
            raise e

    db.add_all(produtos)
    db.commit()
    print(f"{len(produtos)} produtos inseridos com sucesso.")


def seed_categorias_imagens(db: Session):
    if db.query(CategoriaImagem).first():
        print("Tabela categorias_imagens já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "dim_categoria_imagens.csv"
    rows = read_csv_rows(csv_path)

    categorias_imagens = []
    for index, row in enumerate(rows):
        try:
            categoria_imagem = CategoriaImagem(
                categoria=empty_to_none(row.get("Categoria")),
                link=empty_to_none(row.get("Link")),
            )
            categorias_imagens.append(categoria_imagem)
        except Exception as e:
            print(f"Erro em categorias_imagens na linha {index}: {row}")
            raise e

    db.add_all(categorias_imagens)
    db.commit()
    print(f"{len(categorias_imagens)} categorias de imagens inseridas com sucesso.")


def seed_pedidos(db: Session):
    if db.query(Pedido).first():
        print("Tabela pedidos já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "fat_pedidos.csv"
    rows = read_csv_rows(csv_path)

    pedidos = []
    for index, row in enumerate(rows):
        try:
            pedido = Pedido(
                id_pedido=empty_to_none(row.get("id_pedido")),
                id_consumidor=empty_to_none(row.get("id_consumidor")),
                status=empty_to_none(row.get("status")),
                pedido_compra_timestamp=to_datetime(row.get("pedido_compra_timestamp")),
                pedido_entregue_timestamp=to_datetime(row.get("pedido_entregue_timestamp")),
                data_estimada_entrega=to_date(row.get("data_estimada_entrega")),
                tempo_entrega_dias=to_float(row.get("tempo_entrega_dias")),
                tempo_entrega_estimado_dias=to_float(row.get("tempo_entrega_estimado_dias")),
                diferenca_entrega_dias=to_float(row.get("diferenca_entrega_dias")),
                entrega_no_prazo=empty_to_none(row.get("entrega_no_prazo")),
            )
            pedidos.append(pedido)
        except Exception as e:
            print(f"Erro em pedidos na linha {index}: {row}")
            raise e

    db.add_all(pedidos)
    db.commit()
    print(f"{len(pedidos)} pedidos inseridos com sucesso.")


def seed_itens_pedidos(db: Session):
    if db.query(ItemPedido).first():
        print("Tabela itens_pedidos já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "fat_itens_pedidos.csv"
    rows = read_csv_rows(csv_path)

    itens = []
    for index, row in enumerate(rows):
        try:
            item = ItemPedido(
                id_pedido=empty_to_none(row.get("id_pedido")),
                id_item=to_int(row.get("id_item")),
                id_produto=empty_to_none(row.get("id_produto")),
                id_vendedor=empty_to_none(row.get("id_vendedor")),
                preco_BRL=to_float(row.get("preco_BRL")),
                preco_frete=to_float(row.get("preco_frete")),
            )
            itens.append(item)
        except Exception as e:
            print(f"Erro em itens_pedidos na linha {index}: {row}")
            raise e

    db.add_all(itens)
    db.commit()
    print(f"{len(itens)} itens de pedido inseridos com sucesso.")


def seed_avaliacoes_pedidos(db: Session):
    if db.query(AvaliacaoPedido).first():
        print("Tabela avaliacoes_pedidos já possui dados. Seed ignorado.")
        return

    csv_path = DATA_DIR / "fat_avaliacoes_pedidos.csv"
    rows = read_csv_rows(csv_path)

    avaliacoes = []
    ids_vistos = set()

    for index, row in enumerate(rows):
        try:
            id_avaliacao = empty_to_none(row.get("id_avaliacao"))

            if id_avaliacao in ids_vistos:
                continue

            ids_vistos.add(id_avaliacao)

            avaliacao = AvaliacaoPedido(
                id_avaliacao=id_avaliacao,
                id_pedido=empty_to_none(row.get("id_pedido")),
                avaliacao=to_int(row.get("avaliacao")),
                titulo_comentario=empty_to_none(row.get("titulo_comentario")) or "Sem título",
                comentario=empty_to_none(row.get("comentario")) or "Sem comentário",
                data_comentario=to_datetime(row.get("data_comentario")),
                data_resposta=to_datetime(row.get("data_resposta")),
            )
            avaliacoes.append(avaliacao)
        except Exception as e:
            print(f"Erro em avaliacoes_pedidos na linha {index}: {row}")
            raise e

    db.add_all(avaliacoes)
    db.commit()
    print(f"{len(avaliacoes)} avaliações de pedidos inseridas com sucesso.")


def main():
    db = SessionLocal()
    try:
        seed_vendedores(db)
        seed_consumidores(db)
        seed_produtos(db)
        seed_categorias_imagens(db)
        seed_pedidos(db)
        seed_itens_pedidos(db)
        seed_avaliacoes_pedidos(db)
        print("Seed finalizado com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()