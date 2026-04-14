import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.vendedor import Vendedor
from app.repositories import vendedor as vendedor_repository
from app.schemas.vendedor import (
    VendedorCreate,
    VendedorResponse,
    VendedorUpdate,
)


# Arquivo para gerenciar a lógica de negócio relacionada aos vendedores


def listar_vendedores(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[VendedorResponse]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    vendedores = vendedor_repository.listar_vendedores(db, limit=limit, offset=offset)
    return [VendedorResponse.model_validate(vendedor) for vendedor in vendedores]


def buscar_vendedor_por_id(
    db: Session,
    id_vendedor: str,
) -> VendedorResponse:
    id_vendedor = id_vendedor.strip()

    vendedor = vendedor_repository.buscar_vendedor_por_id(db, id_vendedor)

    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado.",
        )

    return VendedorResponse.model_validate(vendedor)


def buscar_vendedores_por_termo(
    db: Session,
    termo: str,
    limit: int = 50,
    offset: int = 0,
) -> list[VendedorResponse]:
    termo = termo.strip()
    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    if not termo:
        return []

    vendedores = vendedor_repository.buscar_vendedores_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )
    return [VendedorResponse.model_validate(vendedor) for vendedor in vendedores]


def criar_vendedor(
    db: Session,
    vendedor_data: VendedorCreate,
) -> VendedorResponse:
    vendedor_duplicado = vendedor_repository.buscar_vendedor_duplicado(
        db=db,
        nome_vendedor=vendedor_data.nome_vendedor,
        prefixo_cep=vendedor_data.prefixo_cep,
        cidade=vendedor_data.cidade,
        estado=vendedor_data.estado,
    )

    if vendedor_duplicado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um vendedor com as mesmas características.",
        )

    vendedor = Vendedor(
        id_vendedor=uuid.uuid4().hex,
        nome_vendedor=vendedor_data.nome_vendedor,
        prefixo_cep=vendedor_data.prefixo_cep,
        cidade=vendedor_data.cidade,
        estado=vendedor_data.estado,
    )

    vendedor_criado = vendedor_repository.criar_vendedor(db, vendedor)
    return VendedorResponse.model_validate(vendedor_criado)


def atualizar_vendedor(
    db: Session,
    id_vendedor: str,
    vendedor_data: VendedorUpdate,
) -> VendedorResponse:
    id_vendedor = id_vendedor.strip()

    vendedor = vendedor_repository.buscar_vendedor_por_id(db, id_vendedor)

    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado.",
        )

    dados_atualizacao = vendedor_data.model_dump(exclude_unset=True)

    nome_vendedor = dados_atualizacao.get("nome_vendedor", vendedor.nome_vendedor)
    prefixo_cep = dados_atualizacao.get("prefixo_cep", vendedor.prefixo_cep)
    cidade = dados_atualizacao.get("cidade", vendedor.cidade)
    estado = dados_atualizacao.get("estado", vendedor.estado)

    vendedor_duplicado = vendedor_repository.buscar_vendedor_duplicado(
        db=db,
        nome_vendedor=nome_vendedor,
        prefixo_cep=prefixo_cep,
        cidade=cidade,
        estado=estado,
    )

    if vendedor_duplicado is not None and vendedor_duplicado.id_vendedor != vendedor.id_vendedor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe outro vendedor com as mesmas características.",
        )

    for campo, valor in dados_atualizacao.items():
        setattr(vendedor, campo, valor)

    vendedor_atualizado = vendedor_repository.atualizar_vendedor(db, vendedor)
    return VendedorResponse.model_validate(vendedor_atualizado)


def remover_vendedor(
    db: Session,
    id_vendedor: str,
) -> None:
    id_vendedor = id_vendedor.strip()

    vendedor = vendedor_repository.buscar_vendedor_por_id(db, id_vendedor)

    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado.",
        )

    vendedor_repository.remover_vendedor(db, vendedor)