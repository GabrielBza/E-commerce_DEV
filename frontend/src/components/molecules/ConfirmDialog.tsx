import Button from "../atoms/Button";

type ConfirmDialogProps = {
  open: boolean;
  title: string;
  description: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm: () => void;
  onCancel: () => void;
};

export default function ConfirmDialog({
  open,
  title,
  description,
  confirmText = "Confirmar",
  cancelText = "Cancelar",
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/45 px-4">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-xl">
        <div className="mb-4">
          <h2 className="text-xl font-bold tracking-tight text-slate-900">
            {title}
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-500">
            {description}
          </p>
        </div>

        <div className="flex items-center justify-end gap-3">
          <Button type="button" variant="secondary" onClick={onCancel}>
            {cancelText}
          </Button>

          <Button type="button" variant="danger" onClick={onConfirm}>
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  );
}