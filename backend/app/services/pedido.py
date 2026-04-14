import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.repositories import consumidor as consumidor_repository
from app.repositories import pedido as pedido_repository
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate


# Arquivo para gerenciar a lógica de negócio relacionada aos pedidos


def listar_pedidos(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[PedidoResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    pedidos = pedido_repository.listar_pedidos(db, limit=limit, offset=offset)
    return [PedidoResponse.model_validate(pedido) for pedido in pedidos]


def buscar_pedido_por_id(
    db: Session,
    id_pedido: str,
) -> PedidoResponse:
    id_pedido = id_pedido.strip()

    pedido = pedido_repository.buscar_pedido_por_id(db, id_pedido)

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    return PedidoResponse.model_validate(pedido)


def buscar_pedidos_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[PedidoResponse]:
    termo = termo.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    if not termo:
        return []

    pedidos = pedido_repository.buscar_pedidos_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )
    return [PedidoResponse.model_validate(pedido) for pedido in pedidos]


def listar_pedidos_por_consumidor(
    db: Session,
    id_consumidor: str,
    limit: int = 50,
    offset: int = 0,
) -> list[PedidoResponse]:
    id_consumidor = id_consumidor.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    consumidor = consumidor_repository.buscar_consumidor_por_id(db, id_consumidor)
    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    pedidos = pedido_repository.listar_pedidos_por_consumidor(
        db,
        id_consumidor=id_consumidor,
        limit=limit,
        offset=offset,
    )
    return [PedidoResponse.model_validate(pedido) for pedido in pedidos]


def criar_pedido(
    db: Session,
    pedido_data: PedidoCreate,
) -> PedidoResponse:
    consumidor = consumidor_repository.buscar_consumidor_por_id(db, pedido_data.id_consumidor)

    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    pedido_duplicado = pedido_repository.buscar_pedido_duplicado(
        db=db,
        id_consumidor=pedido_data.id_consumidor,
        status=pedido_data.status,
        pedido_compra_timestamp=pedido_data.pedido_compra_timestamp,
    )

    if pedido_duplicado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um pedido com as mesmas características principais.",
        )

    pedido = Pedido(
        id_pedido=uuid.uuid4().hex,
        id_consumidor=pedido_data.id_consumidor,
        status=pedido_data.status,
        pedido_compra_timestamp=pedido_data.pedido_compra_timestamp,
        pedido_entregue_timestamp=pedido_data.pedido_entregue_timestamp,
        data_estimada_entrega=pedido_data.data_estimada_entrega,
        tempo_entrega_dias=pedido_data.tempo_entrega_dias,
        tempo_entrega_estimado_dias=pedido_data.tempo_entrega_estimado_dias,
        diferenca_entrega_dias=pedido_data.diferenca_entrega_dias,
        entrega_no_prazo=pedido_data.entrega_no_prazo,
    )

    pedido_criado = pedido_repository.criar_pedido(db, pedido)
    return PedidoResponse.model_validate(pedido_criado)


def atualizar_pedido(
    db: Session,
    id_pedido: str,
    pedido_data: PedidoUpdate,
) -> PedidoResponse:
    id_pedido = id_pedido.strip()

    pedido = pedido_repository.buscar_pedido_por_id(db, id_pedido)

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    dados_atualizacao = pedido_data.model_dump(exclude_unset=True)

    novo_id_consumidor = dados_atualizacao.get("id_consumidor", pedido.id_consumidor)
    consumidor = consumidor_repository.buscar_consumidor_por_id(db, novo_id_consumidor)

    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    for campo, valor in dados_atualizacao.items():
        setattr(pedido, campo, valor)

    pedido_atualizado = pedido_repository.atualizar_pedido(db, pedido)
    return PedidoResponse.model_validate(pedido_atualizado)


def remover_pedido(
    db: Session,
    id_pedido: str,
) -> None:
    id_pedido = id_pedido.strip()

    pedido = pedido_repository.buscar_pedido_por_id(db, id_pedido)

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

    pedido_repository.remover_pedido(db, pedido)