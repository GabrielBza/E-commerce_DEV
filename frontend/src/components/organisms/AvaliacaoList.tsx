import type { AvaliacaoProdutoResponse } from "../../types/produto";

type AvaliacaoListProps = {
  avaliacoes: AvaliacaoProdutoResponse[];
};

function formatarData(data: string | null): string {
  if (!data) return "Data indisponível";

  const dataObj = new Date(data);

  return dataObj.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

export default function AvaliacaoList({ avaliacoes }: AvaliacaoListProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-slate-900">
          Avaliações recentes
        </h2>
        <p className="text-sm text-slate-500">
          Feedbacks registrados pelos consumidores para este produto.
        </p>
      </div>

      {avaliacoes.length === 0 ? (
        <div className="rounded-xl bg-slate-50 p-6 text-sm text-slate-500">
          Este produto ainda não possui avaliações.
        </div>
      ) : (
        <div className="space-y-4">
          {avaliacoes.map((avaliacao) => (
            <article
              key={avaliacao.id_avaliacao}
              className="rounded-xl border border-slate-200 bg-slate-50 p-4"
            >
              <div className="mb-2 flex items-center justify-between gap-3">
                <h3 className="text-sm font-semibold text-slate-800">
                  {avaliacao.titulo_comentario || "Sem título"}
                </h3>

                <span className="rounded-full bg-violet-100 px-2.5 py-1 text-xs font-semibold text-violet-700">
                  {avaliacao.avaliacao}★
                </span>
              </div>

              <p className="text-sm leading-relaxed text-slate-600">
                {avaliacao.comentario || "Sem comentário."}
              </p>

              <p className="mt-3 text-xs text-slate-400">
                {formatarData(avaliacao.data_comentario)}
              </p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}