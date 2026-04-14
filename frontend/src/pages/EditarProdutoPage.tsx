import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Button from "../components/atoms/Button";
import Spinner from "../components/atoms/Spinner";
import FeedbackAlert from "../components/molecules/FeedbackAlert";
import ProdutoForm, {
  type ProdutoFormSubmitData,
} from "../components/organisms/ProdutoForm";
import ProdutoFormTemplate from "../components/templates/ProdutoFormTemplate";
import {
  atualizarProduto,
  listarCategoriasProdutos,
} from "../api/produtoService";
import { useProdutoDetalhe } from "../hooks/useProdutoDetalhe";

export default function EditarProdutoPage() {
  const navigate = useNavigate();
  const { idProduto } = useParams();

  const { produto, carregando, erro } = useProdutoDetalhe(idProduto);

  const [categorias, setCategorias] = useState<string[]>([]);
  const [salvando, setSalvando] = useState(false);
  const [erroSalvar, setErroSalvar] = useState("");

  useEffect(() => {
    async function carregarCategorias() {
      try {
        const data = await listarCategoriasProdutos();
        setCategorias(data);
      } catch (error) {
        console.error(error);
      }
    }

    carregarCategorias();
  }, []);

  async function handleSubmit(data: ProdutoFormSubmitData) {
    if (!idProduto) {
      setErroSalvar("Produto não informado.");
      return;
    }

    try {
      setSalvando(true);
      setErroSalvar("");

      const produtoAtualizado = await atualizarProduto(idProduto, data);
      navigate(`/produtos/${produtoAtualizado.id_produto}`);
    } catch (error) {
      console.error(error);
      setErroSalvar("Não foi possível atualizar o produto.");
    } finally {
      setSalvando(false);
    }
  }

  const header = (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-sm font-medium text-violet-600">
            E-Commerce Manager
          </p>
          <h1 className="text-2xl font-bold tracking-tight">Editar produto</h1>
          <p className="mt-1 text-sm text-slate-500">
            Atualize as informações do produto selecionado.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            type="button"
            variant="secondary"
            onClick={() => navigate("/produtos")}
          >
            Voltar ao catálogo
          </Button>

          {produto ? (
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate(`/produtos/${produto.id_produto}`)}
            >
              Ver detalhe
            </Button>
          ) : null}
        </div>
      </div>
    </header>
  );

  const feedback = erroSalvar ? (
    <FeedbackAlert
      title="Erro ao editar produto"
      message={erroSalvar}
      variant="error"
    />
  ) : erro ? (
    <FeedbackAlert
      title="Erro ao carregar produto"
      message={erro}
      variant="error"
    />
  ) : null;

  if (carregando) {
    return (
      <ProdutoFormTemplate
        header={header}
        feedback={
          <section className="rounded-2xl border border-slate-200 bg-white p-10 shadow-sm">
            <div className="flex flex-col items-center justify-center gap-4 text-center">
              <Spinner size="lg" />
              <div>
                <p className="text-sm font-medium text-slate-700">
                  Carregando dados do produto...
                </p>
                <p className="mt-1 text-sm text-slate-500">
                  Aguarde enquanto preparamos o formulário de edição.
                </p>
              </div>
            </div>
          </section>
        }
        form={null}
      />
    );
  }

  if (!produto) {
    return (
      <ProdutoFormTemplate
        header={header}
        feedback={
          feedback || (
            <FeedbackAlert
              title="Produto não encontrado"
              message="Não foi possível localizar o produto para edição."
              variant="info"
            />
          )
        }
        form={null}
      />
    );
  }

  return (
    <ProdutoFormTemplate
      header={header}
      feedback={feedback}
      form={
        <ProdutoForm
          key={produto.id_produto}
          initialData={produto}
          categorias={categorias}
          loading={salvando}
          submitLabel="Salvar alterações"
          onCancel={() => navigate(`/produtos/${produto.id_produto}`)}
          onSubmit={handleSubmit}
        />
      }
    />
  );
}