import Badge from "../atoms/Badge";
import type { ProdutoDetalheResponse } from "../../types/produto";

type ProdutoDetailHeroProps = {
  produto: ProdutoDetalheResponse;
};

function montarDimensoes(produto: ProdutoDetalheResponse): string {
  const comprimento = produto.comprimento_centimetros ?? "-";
  const largura = produto.largura_centimetros ?? "-";
  const altura = produto.altura_centimetros ?? "-";

  return `${comprimento} x ${largura} x ${altura} cm`;
}

export default function ProdutoDetailHero({
  produto,
}: ProdutoDetailHeroProps) {
  return (
    <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="grid gap-0 lg:grid-cols-[1fr_1.2fr]">
        <div className="aspect-[16/11] bg-slate-100">
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

        <div className="p-6">
          <Badge>{produto.categoria_produto}</Badge>

          <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {produto.nome_produto}
          </h1>

          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl bg-slate-50 p-4">
              <p className="text-xs text-slate-500">Peso</p>
              <p className="mt-1 text-sm font-semibold text-slate-900">
                {produto.peso_produto_gramas ?? "-"} g
              </p>
            </div>

            <div className="rounded-xl bg-slate-50 p-4">
              <p className="text-xs text-slate-500">Dimensões</p>
              <p className="mt-1 text-sm font-semibold text-slate-900">
                {montarDimensoes(produto)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}