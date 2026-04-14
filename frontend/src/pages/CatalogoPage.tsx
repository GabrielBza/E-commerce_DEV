import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Spinner from "../components/atoms/Spinner";
import FeedbackAlert from "../components/molecules/FeedbackAlert";
import EmptyState from "../components/molecules/EmptyState";
import PaginationControls from "../components/molecules/PaginationControls";
import SearchBar from "../components/molecules/SearchBar";
import CatalogHeader from "../components/organisms/CatalogHeader";
import ProdutoGrid from "../components/organisms/ProdutoGrid";
import CatalogoTemplate from "../components/templates/CatalogoTemplate";
import {
  buscarProdutosPorTermo,
  listarProdutos,
} from "../api/produtoService";
import type { ProdutoResponse } from "../types/produto";

const LIMITE_POR_PAGINA = 16;

export default function CatalogoPage() {
  const navigate = useNavigate();

  const [produtos, setProdutos] = useState<ProdutoResponse[]>([]);
  const [carregandoInicial, setCarregandoInicial] = useState(true);
  const [atualizandoLista, setAtualizandoLista] = useState(false);
  const [buscando, setBuscando] = useState(false);
  const [erro, setErro] = useState("");
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [termoBuscaAtual, setTermoBuscaAtual] = useState("");

  async function carregarProdutos(
    pagina: number = 1,
    termo: string = "",
    options?: { silencioso?: boolean }
  ) {
    const silencioso = options?.silencioso ?? false;

    try {
      if (silencioso) {
        setAtualizandoLista(true);
      } else {
        setCarregandoInicial(true);
      }

      setErro("");

      const offset = (pagina - 1) * LIMITE_POR_PAGINA;
      const termoNormalizado = termo.trim();

      const data = termoNormalizado
        ? await buscarProdutosPorTermo({
            termo: termoNormalizado,
            limit: LIMITE_POR_PAGINA,
            offset,
          })
        : await listarProdutos({
            limit: LIMITE_POR_PAGINA,
            offset,
          });

      setProdutos(data);
      setPaginaAtual(pagina);
      setTermoBuscaAtual(termoNormalizado);
    } catch (error) {
      console.error(error);
      setErro("Não foi possível carregar o catálogo de produtos.");
    } finally {
      setCarregandoInicial(false);
      setAtualizandoLista(false);
    }
  }

  async function handleBuscar(termo: string) {
    try {
      setBuscando(true);
      await carregarProdutos(1, termo, { silencioso: produtos.length > 0 });
    } finally {
      setBuscando(false);
    }
  }

  function handleVerDetalhes(idProduto: string) {
    navigate(`/produtos/${idProduto}`);
  }

  function handleEditar(idProduto: string) {
    navigate(`/produtos/${idProduto}/editar`);
  }

  function handleNovoProduto() {
    navigate("/produtos/novo");
  }

  function handlePaginaAnterior() {
    if (paginaAtual > 1) {
      carregarProdutos(paginaAtual - 1, termoBuscaAtual, { silencioso: true });
    }
  }

  function handleProximaPagina() {
    if (produtos.length === LIMITE_POR_PAGINA) {
      carregarProdutos(paginaAtual + 1, termoBuscaAtual, { silencioso: true });
    }
  }

  useEffect(() => {
    carregarProdutos(1, "");
  }, []);

  const feedback = erro ? (
    <FeedbackAlert
      title="Erro ao carregar catálogo"
      message={erro}
      variant="error"
    />
  ) : null;

  const content = carregandoInicial ? (
    <section className="rounded-2xl border border-slate-200 bg-white p-10 shadow-sm">
      <div className="flex flex-col items-center justify-center gap-4 text-center">
        <Spinner size="lg" />
        <div>
          <p className="text-sm font-medium text-slate-700">
            Carregando produtos...
          </p>
          <p className="mt-1 text-sm text-slate-500">
            Aguarde enquanto buscamos o catálogo da loja.
          </p>
        </div>
      </div>
    </section>
  ) : produtos.length === 0 ? (
    <EmptyState
      title="Nenhum produto encontrado"
      description="Tente buscar por outro termo ou recarregue o catálogo para visualizar os produtos disponíveis."
      actionLabel="Recarregar catálogo"
      onAction={() => carregarProdutos(1, "")}
    />
  ) : (
    <div className="space-y-6">
      {atualizandoLista ? (
        <div className="flex items-center justify-end gap-2 text-sm text-slate-500">
          <Spinner size="sm" />
          <span>Atualizando lista...</span>
        </div>
      ) : null}

      <ProdutoGrid
        produtos={produtos}
        onVerDetalhes={handleVerDetalhes}
        onEditar={handleEditar}
      />

      <PaginationControls
        paginaAtual={paginaAtual}
        limitePorPagina={LIMITE_POR_PAGINA}
        quantidadeItensAtual={produtos.length}
        onPaginaAnterior={handlePaginaAnterior}
        onProximaPagina={handleProximaPagina}
      />
    </div>
  );

  return (
    <CatalogoTemplate
      header={
        <CatalogHeader
          onAtualizar={() =>
            carregarProdutos(paginaAtual, termoBuscaAtual, {
              silencioso: produtos.length > 0,
            })
          }
          onNovoProduto={handleNovoProduto}
        />
      }
      searchSection={
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h2 className="text-lg font-semibold">Catálogo de produtos</h2>
            <p className="text-sm text-slate-500">
              Navegue pelos produtos cadastrados, busque por nome ou categoria e
              acesse os detalhes.
            </p>
          </div>

          <SearchBar loading={buscando} onSearch={handleBuscar} />
        </div>
      }
      feedback={feedback}
      content={content}
    />
  );
}