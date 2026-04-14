import type { ProdutoDetalheResponse } from "../../types/produto";

type ProdutoStatsProps = {
  produto: ProdutoDetalheResponse;
};

function formatarMoeda(valor: number): string {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

export default function ProdutoStats({ produto }: ProdutoStatsProps) {
  const stats = [
    {
      label: "Quantidade de vendas",
      value: String(produto.quantidade_vendas),
    },
    {
      label: "Valor total vendido",
      value: formatarMoeda(produto.valor_total_vendido),
    },
    {
      label: "Quantidade de avaliações",
      value: String(produto.quantidade_avaliacoes),
    },
    {
      label: "Média das avaliações",
      value:
        produto.media_avaliacoes !== null
          ? produto.media_avaliacoes.toFixed(1)
          : "Sem avaliações",
    },
  ];

  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <article
          key={stat.label}
          className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <p className="text-sm text-slate-500">{stat.label}</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-slate-900">
            {stat.value}
          </p>
        </article>
      ))}
    </section>
  );
}