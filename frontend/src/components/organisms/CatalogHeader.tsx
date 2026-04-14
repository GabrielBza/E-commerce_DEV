import Button from "../atoms/Button";

type CatalogHeaderProps = {
  onAtualizar: () => void;
  onNovoProduto: () => void;
};

export default function CatalogHeader({
  onAtualizar,
  onNovoProduto,
}: CatalogHeaderProps) {
  return (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-sm font-medium text-violet-600">
            E-Commerce Manager
          </p>
          <h1 className="text-2xl font-bold tracking-tight">Produtos</h1>
          <p className="mt-1 text-sm text-slate-500">
            Gerencie o catálogo, pesquise itens e acompanhe os detalhes de cada
            produto.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button type="button" variant="secondary" onClick={onAtualizar}>
            Atualizar catálogo
          </Button>

          <Button type="button" onClick={onNovoProduto}>
            Novo produto
          </Button>
        </div>
      </div>
    </header>
  );
}