import type { ReactNode } from "react";

type FeedbackVariant = "error" | "success" | "info";

type FeedbackAlertProps = {
  title?: string;
  message: string;
  variant?: FeedbackVariant;
  action?: ReactNode;
};

const variantClasses: Record<FeedbackVariant, string> = {
  error: "border-red-200 bg-red-50 text-red-700",
  success: "border-emerald-200 bg-emerald-50 text-emerald-700",
  info: "border-slate-200 bg-slate-50 text-slate-700",
};

export default function FeedbackAlert({
  title,
  message,
  variant = "info",
  action,
}: FeedbackAlertProps) {
  return (
    <section
      className={[
        "rounded-2xl border p-4 shadow-sm",
        variantClasses[variant],
      ].join(" ")}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          {title ? (
            <h3 className="text-sm font-semibold">{title}</h3>
          ) : null}
          <p className={title ? "mt-1 text-sm" : "text-sm"}>{message}</p>
        </div>

        {action ? <div>{action}</div> : null}
      </div>
    </section>
  );
}