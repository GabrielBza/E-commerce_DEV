from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.consumidor import ConsumidorCreate, ConsumidorResponse, ConsumidorUpdate
from app.services import consumidor as consumidor_service

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])


# Arquivo que define as rotas relacionadas aos consumidores


@router.get("", response_model=list[ConsumidorResponse])
def listar_consumidores(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return consumidor_service.listar_consumidores(db, limit=limit, offset=offset)


@router.get("/busca", response_model=list[ConsumidorResponse])
def buscar_consumidores_por_termo(
    termo: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return consumidor_service.buscar_consumidores_por_termo(
        db,
        termo=termo,
        limit=limit,
        offset=offset,
    )


@router.get("/{id_consumidor}", response_model=ConsumidorResponse)
def buscar_consumidor_por_id(
    id_consumidor: str,
    db: Session = Depends(get_db),
):
    return consumidor_service.buscar_consumidor_por_id(db, id_consumidor)


@router.post("", response_model=ConsumidorResponse, status_code=status.HTTP_201_CREATED)
def criar_consumidor(
    consumidor_data: ConsumidorCreate,
    db: Session = Depends(get_db),
):
    return consumidor_service.criar_consumidor(db, consumidor_data)


@router.put("/{id_consumidor}", response_model=ConsumidorResponse)
def atualizar_consumidor(
    id_consumidor: str,
    consumidor_data: ConsumidorUpdate,
    db: Session = Depends(get_db),
):
    return consumidor_service.atualizar_consumidor(db, id_consumidor, consumidor_data)


@router.delete("/{id_consumidor}", status_code=status.HTTP_204_NO_CONTENT)
def remover_consumidor(
    id_consumidor: str,
    db: Session = Depends(get_db),
):
    consumidor_service.remover_consumidor(db, id_consumidor)
    return Response(status_code=status.HTTP_204_NO_CONTENT)