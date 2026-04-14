from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# Novo model para guardar os links das imagens das categorias
class CategoriaImagem(Base):
    __tablename__ = "categorias_imagens"

    categoria: Mapped[str] = mapped_column(String(100), primary_key=True)
    link: Mapped[str] = mapped_column(String(1000), nullable=False)