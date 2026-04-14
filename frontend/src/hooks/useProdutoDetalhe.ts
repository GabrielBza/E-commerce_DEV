import { useCallback, useEffect, useState } from "react";

import { buscarDetalheProduto } from "../api/produtoService";
import type { ProdutoDetalheResponse } from "../types/produto";

type UseProdutoDetalheResult = {
  produto: ProdutoDetalheResponse | null;
  carregando: boolean;
  erro: string;
  recarregar: () => Promise<void>;
};

export function useProdutoDetalhe(
  idProduto?: string
): UseProdutoDetalheResult {
  const [produto, setProduto] = useState<ProdutoDetalheResponse | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  const recarregar = useCallback(async () => {
    if (!idProduto) {
      setErro("Produto não informado.");
      setProduto(null);
      setCarregando(false);
      return;
    }

    try {
      setCarregando(true);
      setErro("");

      const data = await buscarDetalheProduto(idProduto);
      setProduto(data);
    } catch (error) {
      console.error(error);
      setErro("Não foi possível carregar os detalhes do produto.");
      setProduto(null);
    } finally {
      setCarregando(false);
    }
  }, [idProduto]);

  useEffect(() => {
    recarregar();
  }, [recarregar]);

  return {
    produto,
    carregando,
    erro,
    recarregar,
  };
}