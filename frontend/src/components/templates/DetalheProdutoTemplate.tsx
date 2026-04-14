import type { ReactNode } from "react";

type DetalheProdutoTemplateProps = {
  header: ReactNode;
  hero: ReactNode;
  stats: ReactNode;
  avaliacoes: ReactNode;
  feedback?: ReactNode;
};

export default function DetalheProdutoTemplate({
  header,
  hero,
  stats,
  avaliacoes,
  feedback,
}: DetalheProdutoTemplateProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {header}

      <main className="mx-auto flex max-w-7xl flex-col gap-6 px-6 py-8">
        {feedback ? feedback : null}
        {hero}
        {stats}
        {avaliacoes}
      </main>
    </div>
  );
}