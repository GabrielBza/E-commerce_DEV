import type { ReactNode } from "react";

type ProdutoFormTemplateProps = {
  header: ReactNode;
  form: ReactNode;
  feedback?: ReactNode;
};

export default function ProdutoFormTemplate({
  header,
  form,
  feedback,
}: ProdutoFormTemplateProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {header}

      <main className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-8">
        {feedback ? feedback : null}
        {form}
      </main>
    </div>
  );
}