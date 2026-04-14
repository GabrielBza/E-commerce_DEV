import api from "./axios";
import type {
  ProdutoCreate,
  ProdutoDetalheResponse,
  ProdutoResponse,
  ProdutoUpdate,
} from "../types/produto";

type ListarProdutosParams = {
  limit?: number;
  offset?: number;
};

type BuscarProdutosParams = {
  termo: string;
  limit?: number;
  offset?: number;
};

export async function listarProdutos(
  params: ListarProdutosParams = {}
): Promise<ProdutoResponse[]> {
  const { limit = 50, offset = 0 } = params;

  const response = await api.get<ProdutoResponse[]>("/produtos", {
    params: { limit, offset },
  });

  return response.data;
}

export async function buscarProdutosPorTermo(
  params: BuscarProdutosParams
): Promise<ProdutoResponse[]> {
  const { termo, limit = 50, offset = 0 } = params;

  const response = await api.get<ProdutoResponse[]>("/produtos/busca", {
    params: { termo, limit, offset },
  });

  return response.data;
}

export async function buscarDetalheProduto(
  idProduto: string
): Promise<ProdutoDetalheResponse> {
  const response = await api.get<ProdutoDetalheResponse>(`/produtos/${idProduto}`);
  return response.data;
}

export async function criarProduto(
  produto: ProdutoCreate
): Promise<ProdutoResponse> {
  const response = await api.post<ProdutoResponse>("/produtos", produto);
  return response.data;
}

export async function atualizarProduto(
  idProduto: string,
  produto: ProdutoUpdate
): Promise<ProdutoResponse> {
  const response = await api.put<ProdutoResponse>(`/produtos/${idProduto}`, produto);
  return response.data;
}

export async function removerProduto(idProduto: string): Promise<void> {
  await api.delete(`/produtos/${idProduto}`);
}

export async function listarCategoriasProdutos(): Promise<string[]> {
  const response = await api.get<string[]>("/produtos/categorias");
  return response.data;
}