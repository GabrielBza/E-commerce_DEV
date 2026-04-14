import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Button from "../components/atoms/Button";
import FeedbackAlert from "../components/molecules/FeedbackAlert";
import ProdutoForm, {
  type ProdutoFormSubmitData,
} from "../components/organisms/ProdutoForm";
import ProdutoFormTemplate from "../components/templates/ProdutoFormTemplate";
import {
  criarProduto,
  listarCategoriasProdutos,
} from "../api/produtoService";

export default function NovoProdutoPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [categorias, setCategorias] = useState<string[]>([]);

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
    try {
      setLoading(true);
      setErro("");

      const produto = await criarProduto(data);
      navigate(`/produtos/${produto.id_produto}`);
    } catch (error) {
      console.error(error);
      setErro("Não foi possível criar o produto.");
    } finally {
      setLoading(false);
    }
  }

  const header = (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-sm font-medium text-violet-600">
            E-Commerce Manager
          </p>
          <h1 className="text-2xl font-bold tracking-tight">Novo produto</h1>
          <p className="mt-1 text-sm text-slate-500">
            Cadastre um novo produto no catálogo da loja.
          </p>
        </div>

        <Button
          type="button"
          variant="secondary"
          onClick={() => navigate("/produtos")}
        >
          Voltar
        </Button>
      </div>
    </header>
  );

  const feedback = erro ? (
    <FeedbackAlert
      title="Erro ao criar produto"
      message={erro}
      variant="error"
    />
  ) : null;

  return (
    <ProdutoFormTemplate
      header={header}
      feedback={feedback}
      form={
        <ProdutoForm
          categorias={categorias}
          loading={loading}
          submitLabel="Criar produto"
          onCancel={() => navigate("/produtos")}
          onSubmit={handleSubmit}
        />
      }
    />
  );
}