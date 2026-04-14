import type { ReactNode } from "react";

type BadgeVariant = "category" | "neutral";

type BadgeProps = {
  children: ReactNode;
  variant?: BadgeVariant;
};

const variantClasses: Record<BadgeVariant, string> = {
  category: "bg-violet-50 text-violet-700",
  neutral: "bg-slate-100 text-slate-700",
};

export default function Badge({
  children,
  variant = "category",
}: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex rounded-full px-3 py-1 text-xs font-medium",
        variantClasses[variant],
      ].join(" ")}
    >
      {children}
    </span>
  );
}