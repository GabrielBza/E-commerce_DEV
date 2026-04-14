import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.consumidor import Consumidor
from app.repositories import consumidor as consumidor_repository
from app.schemas.consumidor import (
    ConsumidorCreate,
    ConsumidorResponse,
    ConsumidorUpdate,
)


# Arquivo para gerenciar a lógica de negócio relacionada aos consumidores


def listar_consumidores(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[ConsumidorResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    consumidores = consumidor_repository.listar_consumidores(db, limit=limit, offset=offset)
    return [ConsumidorResponse.model_validate(consumidor) for consumidor in consumidores]


def buscar_consumidor_por_id(
    db: Session,
    id_consumidor: str,
) -> ConsumidorResponse:
    id_consumidor = id_consumidor.strip()

    consumidor = consumidor_repository.buscar_consumidor_por_id(db, id_consumidor)

    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    return ConsumidorResponse.model_validate(consumidor)


def buscar_consumidores_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[ConsumidorResponse]:
    termo = termo.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    if not termo:
        return []

    consumidores = consumidor_repository.buscar_consumidores_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )
    return [ConsumidorResponse.model_validate(consumidor) for consumidor in consumidores]


def criar_consumidor(
    db: Session,
    consumidor_data: ConsumidorCreate,
) -> ConsumidorResponse:
    consumidor_duplicado = consumidor_repository.buscar_consumidor_duplicado(
        db=db,
        prefixo_cep=consumidor_data.prefixo_cep,
        nome_consumidor=consumidor_data.nome_consumidor,
        cidade=consumidor_data.cidade,
        estado=consumidor_data.estado,
    )

    if consumidor_duplicado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um consumidor com as mesmas características.",
        )

    consumidor = Consumidor(
        id_consumidor=uuid.uuid4().hex,
        prefixo_cep=consumidor_data.prefixo_cep,
        nome_consumidor=consumidor_data.nome_consumidor,
        cidade=consumidor_data.cidade,
        estado=consumidor_data.estado,
    )

    consumidor_criado = consumidor_repository.criar_consumidor(db, consumidor)
    return ConsumidorResponse.model_validate(consumidor_criado)


def atualizar_consumidor(
    db: Session,
    id_consumidor: str,
    consumidor_data: ConsumidorUpdate,
) -> ConsumidorResponse:
    id_consumidor = id_consumidor.strip()

    consumidor = consumidor_repository.buscar_consumidor_por_id(db, id_consumidor)

    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    dados_atualizacao = consumidor_data.model_dump(exclude_unset=True)

    prefixo_cep = dados_atualizacao.get("prefixo_cep", consumidor.prefixo_cep)
    nome_consumidor = dados_atualizacao.get("nome_consumidor", consumidor.nome_consumidor)
    cidade = dados_atualizacao.get("cidade", consumidor.cidade)
    estado = dados_atualizacao.get("estado", consumidor.estado)

    consumidor_duplicado = consumidor_repository.buscar_consumidor_duplicado(
        db=db,
        prefixo_cep=prefixo_cep,
        nome_consumidor=nome_consumidor,
        cidade=cidade,
        estado=estado,
    )

    if consumidor_duplicado is not None and consumidor_duplicado.id_consumidor != consumidor.id_consumidor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe outro consumidor com as mesmas características.",
        )

    for campo, valor in dados_atualizacao.items():
        setattr(consumidor, campo, valor)

    consumidor_atualizado = consumidor_repository.atualizar_consumidor(db, consumidor)
    return ConsumidorResponse.model_validate(consumidor_atualizado)


def remover_consumidor(
    db: Session,
    id_consumidor: str,
) -> None:
    id_consumidor = id_consumidor.strip()

    consumidor = consumidor_repository.buscar_consumidor_por_id(db, id_consumidor)

    if consumidor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado.",
        )

    consumidor_repository.remover_consumidor(db, consumidor)