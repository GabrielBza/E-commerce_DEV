export type ProdutoResponse = {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: number | null;
  comprimento_centimetros: number | null;
  altura_centimetros: number | null;
  largura_centimetros: number | null;
  imagem_categoria: string | null;
};

export type AvaliacaoProdutoResponse = {
  id_avaliacao: string;
  id_pedido: string;
  avaliacao: number;
  titulo_comentario: string | null;
  comentario: string | null;
  data_comentario: string | null;
  data_resposta: string | null;
};

export type ProdutoDetalheResponse = {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: number | null;
  comprimento_centimetros: number | null;
  altura_centimetros: number | null;
  largura_centimetros: number | null;
  quantidade_vendas: number;
  valor_total_vendido: number;
  quantidade_avaliacoes: number;
  media_avaliacoes: number | null;
  avaliacoes: AvaliacaoProdutoResponse[];
  imagem_categoria: string | null;
};

export type ProdutoCreate = {
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas?: number | null;
  comprimento_centimetros?: number | null;
  altura_centimetros?: number | null;
  largura_centimetros?: number | null;
};

export type ProdutoUpdate = {
  nome_produto?: string | null;
  categoria_produto?: string | null;
  peso_produto_gramas?: number | null;
  comprimento_centimetros?: number | null;
  altura_centimetros?: number | null;
  largura_centimetros?: number | null;
};

export type ProdutoFormSubmitData = {
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: number | null;
  comprimento_centimetros: number | null;
  altura_centimetros: number | null;
  largura_centimetros: number | null;
};