import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Button from "../components/atoms/Button";
import Spinner from "../components/atoms/Spinner";
import FeedbackAlert from "../components/molecules/FeedbackAlert";
import ConfirmDialog from "../components/molecules/ConfirmDialog";
import ProdutoDetailHero from "../components/organisms/ProdutoDetailHero";
import ProdutoStats from "../components/organisms/ProdutoStats";
import AvaliacaoList from "../components/organisms/AvaliacaoList";
import DetalheProdutoTemplate from "../components/templates/DetalheProdutoTemplate";
import { removerProduto } from "../api/produtoService";
import { useProdutoDetalhe } from "../hooks/useProdutoDetalhe";

export default function DetalheProdutoPage() {
  const navigate = useNavigate();
  const { idProduto } = useParams();
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);

  const { produto, carregando, erro } = useProdutoDetalhe(idProduto);

  async function handleExcluirProduto() {
    if (!produto) return;

    try {
      await removerProduto(produto.id_produto);
      setConfirmDialogOpen(false);
      navigate("/produtos");
    } catch (error) {
      console.error(error);
    }
  }

  const header = (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-sm font-medium text-violet-600">
            E-Commerce Manager
          </p>
          <h1 className="text-2xl font-bold tracking-tight">
            Detalhe do produto
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Visualize medidas, vendas e avaliações do produto selecionado.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            type="button"
            variant="secondary"
            onClick={() => navigate("/produtos")}
          >
            Voltar
          </Button>

          {produto ? (
            <>
              <Button
                type="button"
                onClick={() => navigate(`/produtos/${produto.id_produto}/editar`)}
              >
                Editar produto
              </Button>

              <Button
                type="button"
                variant="danger"
                onClick={() => setConfirmDialogOpen(true)}
              >
                Excluir produto
              </Button>
            </>
          ) : null}
        </div>
      </div>
    </header>
  );

  const feedback = erro ? (
    <FeedbackAlert
      title="Erro ao carregar produto"
      message={erro}
      variant="error"
    />
  ) : null;

  if (carregando) {
    return (
      <>
        <DetalheProdutoTemplate
          header={header}
          feedback={
            <section className="rounded-2xl border border-slate-200 bg-white p-10 shadow-sm">
              <div className="flex flex-col items-center justify-center gap-4 text-center">
                <Spinner size="lg" />
                <div>
                  <p className="text-sm font-medium text-slate-700">
                    Carregando detalhes do produto...
                  </p>
                  <p className="mt-1 text-sm text-slate-500">
                    Aguarde enquanto buscamos as informações do produto.
                  </p>
                </div>
              </div>
            </section>
          }
          hero={null}
          stats={null}
          avaliacoes={null}
        />

        <ConfirmDialog
          open={confirmDialogOpen}
          title="Excluir produto"
          description="Tem certeza que deseja excluir este produto? Essa ação não poderá ser desfeita."
          confirmText="Excluir"
          cancelText="Cancelar"
          onConfirm={handleExcluirProduto}
          onCancel={() => setConfirmDialogOpen(false)}
        />
      </>
    );
  }

  if (!produto) {
    return (
      <>
        <DetalheProdutoTemplate
          header={header}
          feedback={
            feedback || (
              <FeedbackAlert
                title="Produto não encontrado"
                message="Não foi possível localizar o produto solicitado."
                variant="info"
              />
            )
          }
          hero={null}
          stats={null}
          avaliacoes={null}
        />

        <ConfirmDialog
          open={confirmDialogOpen}
          title="Excluir produto"
          description="Tem certeza que deseja excluir este produto? Essa ação não poderá ser desfeita."
          confirmText="Excluir"
          cancelText="Cancelar"
          onConfirm={handleExcluirProduto}
          onCancel={() => setConfirmDialogOpen(false)}
        />
      </>
    );
  }

  return (
    <>
      <DetalheProdutoTemplate
        header={header}
        feedback={feedback}
        hero={<ProdutoDetailHero produto={produto} />}
        stats={<ProdutoStats produto={produto} />}
        avaliacoes={<AvaliacaoList avaliacoes={produto.avaliacoes} />}
      />

      <ConfirmDialog
        open={confirmDialogOpen}
        title="Excluir produto"
        description="Tem certeza que deseja excluir este produto? Essa ação não poderá ser desfeita."
        confirmText="Excluir"
        cancelText="Cancelar"
        onConfirm={handleExcluirProduto}
        onCancel={() => setConfirmDialogOpen(false)}
      />
    </>
  );
}