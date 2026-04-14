import Badge from "../atoms/Badge";
import Button from "../atoms/Button";
import type { ProdutoResponse } from "../../types/produto";

type ProdutoCardProps = {
  produto: ProdutoResponse;
  onVerDetalhes: (idProduto: string) => void;
  onEditar: (idProduto: string) => void;
};

function montarDimensoes(produto: ProdutoResponse): string {
  const comprimento = produto.comprimento_centimetros ?? "-";
  const largura = produto.largura_centimetros ?? "-";
  const altura = produto.altura_centimetros ?? "-";

  return `${comprimento} x ${largura} x ${altura} cm`;
}

export default function ProdutoCard({
  produto,
  onVerDetalhes,
  onEditar,
}: ProdutoCardProps) {
  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="aspect-[16/10] w-full overflow-hidden bg-slate-100">
        {produto.imagem_categoria ? (
          <img
            src={produto.imagem_categoria}
            alt={produto.categoria_produto}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-sm text-slate-400">
            Sem imagem
          </div>
        )}
      </div>

      <div className="p-5">
        <div className="mb-3 flex items-start justify-between gap-3">
          <div>
            <Badge>{produto.categoria_produto}</Badge>
            <h3 className="mt-3 text-lg font-semibold leading-tight text-slate-900">
              {produto.nome_produto}
            </h3>
          </div>
        </div>

        <div className="mb-5 rounded-xl bg-slate-50 p-4">
          <p className="text-xs text-slate-500">Medidas</p>
          <p className="mt-1 text-sm font-medium text-slate-800">
            {montarDimensoes(produto)}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            type="button"
            variant="secondary"
            fullWidth
            onClick={() => onEditar(produto.id_produto)}
          >
            Editar
          </Button>

          <Button
            type="button"
            fullWidth
            onClick={() => onVerDetalhes(produto.id_produto)}
          >
            Ver detalhes
          </Button>
        </div>
      </div>
    </article>
  );
}