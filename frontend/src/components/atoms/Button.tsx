import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "dark" | "danger";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: ButtonVariant;
  fullWidth?: boolean;
};

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    "bg-violet-600 text-white hover:bg-violet-700 border border-violet-600",
  secondary:
    "bg-white text-slate-700 hover:bg-slate-50 border border-slate-200",
  dark:
    "bg-slate-900 text-white hover:bg-slate-800 border border-slate-900",
  danger:
    "bg-red-600 text-white hover:bg-red-700 border border-red-600",
};

export default function Button({
  children,
  variant = "primary",
  fullWidth = false,
  className = "",
  ...props
}: ButtonProps) {
  return (
    <button
      className={[
        "rounded-xl px-4 py-2 text-sm font-medium shadow-sm transition disabled:cursor-not-allowed disabled:opacity-70",
        variantClasses[variant],
        fullWidth ? "w-full" : "",
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
}