type PaginationControlsProps = {
  paginaAtual: number;
  limitePorPagina: number;
  quantidadeItensAtual: number;
  onPaginaAnterior: () => void;
  onProximaPagina: () => void;
};

export default function PaginationControls({
  paginaAtual,
  limitePorPagina,
  quantidadeItensAtual,
  onPaginaAnterior,
  onProximaPagina,
}: PaginationControlsProps) {
  const inicio = (paginaAtual - 1) * limitePorPagina + 1;
  const fim = (paginaAtual - 1) * limitePorPagina + quantidadeItensAtual;

  const podeVoltar = paginaAtual > 1;
  const podeAvancar = quantidadeItensAtual === limitePorPagina;

  return (
    <section className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm text-slate-500">Resultados exibidos</p>
        <p className="mt-1 text-sm font-medium text-slate-800">
          Mostrando <span className="font-semibold">{inicio}</span>–<span className="font-semibold">{fim}</span>
        </p>
      </div>

      <div className="flex items-center justify-between gap-3 sm:justify-end">
        <button
          type="button"
          onClick={onPaginaAnterior}
          disabled={!podeVoltar}
          className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Anterior
        </button>

        <div className="rounded-xl bg-violet-50 px-4 py-2 text-sm font-semibold text-violet-700">
          Página {paginaAtual}
        </div>

        <button
          type="button"
          onClick={onProximaPagina}
          disabled={!podeAvancar}
          className="rounded-xl bg-violet-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Próxima
        </button>
      </div>
    </section>
  );
}