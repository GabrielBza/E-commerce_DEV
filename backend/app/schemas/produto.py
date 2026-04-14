from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict

# Arquivo que define os modelos de entrada e de saída dos produtos
# Responsável por validar e estruturar os dados que trafegam entre o cliente e o backend
# Regras de preenchimento de campos e de entradas de texto

# Função simples que retorna strings após aplicação de strip ou valores nullos caso a string seja vazia ou nula
def normalizar_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None

# Modelo de base do produto, juntamente com uma validação que não permite que campos obrigatórios sejam vazios ou nulos
class ProdutoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_produto: str = Field(..., min_length=1, max_length=255)
    categoria_produto: str = Field(..., min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

    @field_validator("nome_produto", "categoria_produto", mode="before")
    @classmethod
    def strip_string_obrigatoria(cls, value: Optional[str]) -> str:
        value = normalizar_string(value)
        if value is None:
            raise ValueError("Campo obrigatório não pode ser vazio.")
        return value

# Apenas uma separação de modelo para criar um produto (sem o campo de id que é grado automaticamente)
class ProdutoCreate(ProdutoBase):
    pass

# Modelo de atualização do produto, onde os campos são opcionais, mas caso sejam enviados, não podem ser vazios ou nulos
class ProdutoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome_produto: Optional[str] = Field(None, min_length=1, max_length=255)
    categoria_produto: Optional[str] = Field(None, min_length=1, max_length=100)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)

    @field_validator("nome_produto", "categoria_produto", mode="before")
    @classmethod
    def strip_string_opcional(cls, value: Optional[str]) -> Optional[str]:
        return normalizar_string(value)

# Modelo de resposta do produto, onde o id é incluído e os campos são retornados exatamente como estão no banco de dados
class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_produto: str
    nome_produto: str
    categoria_produto: str
    peso_produto_gramas: Optional[float]
    comprimento_centimetros: Optional[float]
    altura_centimetros: Optional[float]
    largura_centimetros: Optional[float]
    imagem_categoria: Optional[str] = None

# Modelo de resposta das avaliações do produto, onde são retornados os campos relacionados à avaliação
class AvaliacaoProdutoResponse(BaseModel):
    id_avaliacao: str
    id_pedido: str
    avaliacao: int
    titulo_comentario: Optional[str]
    comentario: Optional[str]
    data_comentario: Optional[str]
    data_resposta: Optional[str]

# Modelo de resposta detalhada do produto, onde além dos campos básicos, são incluídas métricas de vendas e 
# avaliações (Algumas avaliações também são incluídas)
class ProdutoDetalheResponse(BaseModel):
    id_produto: str
    nome_produto: str
    categoria_produto: str
    peso_produto_gramas: Optional[float]
    comprimento_centimetros: Optional[float]
    altura_centimetros: Optional[float]
    largura_centimetros: Optional[float]

    quantidade_vendas: int
    valor_total_vendido: float
    quantidade_avaliacoes: int
    media_avaliacoes: Optional[float]

    avaliacoes: list[AvaliacaoProdutoResponse]

    imagem_categoria: Optional[str] = None