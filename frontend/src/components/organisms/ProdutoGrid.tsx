import type { ProdutoResponse } from "../../types/produto";
import ProdutoCard from "./ProdutoCard";

type ProdutoGridProps = {
  produtos: ProdutoResponse[];
  onVerDetalhes: (idProduto: string) => void;
  onEditar: (idProduto: string) => void;
};

export default function ProdutoGrid({
  produtos,
  onVerDetalhes,
  onEditar,
}: ProdutoGridProps) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {produtos.map((produto) => (
        <ProdutoCard
          key={produto.id_produto}
          produto={produto}
          onVerDetalhes={onVerDetalhes}
          onEditar={onEditar}
        />
      ))}
    </section>
  );
}