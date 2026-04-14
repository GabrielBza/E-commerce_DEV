import type { ReactNode } from "react";

type CatalogoTemplateProps = {
  header: ReactNode;
  searchSection: ReactNode;
  content: ReactNode;
  feedback?: ReactNode;
};

export default function CatalogoTemplate({
  header,
  searchSection,
  content,
  feedback,
}: CatalogoTemplateProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {header}

      <main className="mx-auto max-w-7xl px-6 py-8">
        <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          {searchSection}
        </section>

        {feedback ? <section className="mb-6">{feedback}</section> : null}

        {content}
      </main>
    </div>
  );
}