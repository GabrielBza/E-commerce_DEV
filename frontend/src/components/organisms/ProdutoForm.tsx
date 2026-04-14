import { useState } from "react";
import type { ReactNode } from "react";

import Button from "../atoms/Button";
import Input from "../atoms/Input";

type ProdutoFormData = {
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: string;
  comprimento_centimetros: string;
  altura_centimetros: string;
  largura_centimetros: string;
};

export type ProdutoFormSubmitData = {
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas: number | null;
  comprimento_centimetros: number | null;
  altura_centimetros: number | null;
  largura_centimetros: number | null;
};

type ProdutoFormProps = {
  initialData?: {
    nome_produto?: string | null;
    categoria_produto?: string | null;
    peso_produto_gramas?: number | null;
    comprimento_centimetros?: number | null;
    altura_centimetros?: number | null;
    largura_centimetros?: number | null;
  };
  categorias?: string[];
  loading?: boolean;
  submitLabel?: string;
  onCancel: () => void;
  onSubmit: (data: ProdutoFormSubmitData) => void;
};

function numberToString(value?: number | null): string {
  return value !== null && value !== undefined ? String(value) : "";
}

function buildInitialFormData(
  initialData?: ProdutoFormProps["initialData"]
): ProdutoFormData {
  return {
    nome_produto: initialData?.nome_produto ?? "",
    categoria_produto: initialData?.categoria_produto ?? "",
    peso_produto_gramas: numberToString(initialData?.peso_produto_gramas),
    comprimento_centimetros: numberToString(initialData?.comprimento_centimetros),
    altura_centimetros: numberToString(initialData?.altura_centimetros),
    largura_centimetros: numberToString(initialData?.largura_centimetros),
  };
}

export default function ProdutoForm({
  initialData,
  categorias = [],
  loading = false,
  submitLabel = "Salvar",
  onCancel,
  onSubmit,
}: ProdutoFormProps) {
  const [formData, setFormData] = useState<ProdutoFormData>(() =>
    buildInitialFormData(initialData)
  );

  function handleChange(field: keyof ProdutoFormData, value: string) {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  }

  function toNullableNumber(value: string): number | null {
    const normalized = value.trim();
    return normalized === "" ? null : Number(normalized);
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const payload: ProdutoFormSubmitData = {
      nome_produto: formData.nome_produto.trim(),
      categoria_produto: formData.categoria_produto.trim(),
      peso_produto_gramas: toNullableNumber(formData.peso_produto_gramas),
      comprimento_centimetros: toNullableNumber(formData.comprimento_centimetros),
      altura_centimetros: toNullableNumber(formData.altura_centimetros),
      largura_centimetros: toNullableNumber(formData.largura_centimetros),
    };

    onSubmit(payload);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
    >
      <div className="grid gap-5 md:grid-cols-2">
        <Field label="Nome do produto">
          <Input
            value={formData.nome_produto}
            onChange={(e) => handleChange("nome_produto", e.target.value)}
            placeholder="Ex.: Mouse Gamer RGB"
            required
          />
        </Field>

        <Field label="Categoria">
          <>
            <Input
              value={formData.categoria_produto}
              onChange={(e) => handleChange("categoria_produto", e.target.value)}
              placeholder="Digite ou selecione uma categoria"
              list="categorias-produtos"
              required
            />
            <datalist id="categorias-produtos">
              {categorias.map((categoria) => (
                <option key={categoria} value={categoria} />
              ))}
            </datalist>
          </>
        </Field>

        <Field label="Peso (gramas)">
          <Input
            type="number"
            min="0"
            value={formData.peso_produto_gramas}
            onChange={(e) => handleChange("peso_produto_gramas", e.target.value)}
            placeholder="Ex.: 250"
          />
        </Field>

        <Field label="Comprimento (cm)">
          <Input
            type="number"
            min="0"
            value={formData.comprimento_centimetros}
            onChange={(e) => handleChange("comprimento_centimetros", e.target.value)}
            placeholder="Ex.: 15"
          />
        </Field>

        <Field label="Altura (cm)">
          <Input
            type="number"
            min="0"
            value={formData.altura_centimetros}
            onChange={(e) => handleChange("altura_centimetros", e.target.value)}
            placeholder="Ex.: 4"
          />
        </Field>

        <Field label="Largura (cm)">
          <Input
            type="number"
            min="0"
            value={formData.largura_centimetros}
            onChange={(e) => handleChange("largura_centimetros", e.target.value)}
            placeholder="Ex.: 10"
          />
        </Field>
      </div>

      <div className="mt-6 flex items-center justify-end gap-3">
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancelar
        </Button>

        <Button type="submit" disabled={loading}>
          {loading ? "Salvando..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}

type FieldProps = {
  label: string;
  children: ReactNode;
};

function Field({ label, children }: FieldProps) {
  return (
    <label className="flex flex-col gap-2">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      {children}
    </label>
  );
}