import type { FormResult } from "../../types/shared";

type FormIndicatorProps = {
  form: FormResult[];
  labels: {
    W: string;
    D: string;
    L: string;
  };
  recentFormLabel: string;
};

export function FormIndicator({
  form,
  labels,
  recentFormLabel,
}: FormIndicatorProps) {
  return (
    <div
      className="flex items-center justify-center gap-0.5"
      aria-label={recentFormLabel}
    >
      {form.map((result, index) => (
        <span
          aria-label={labels[result]}
          className={`inline-block h-2 w-2 rounded-full ${
            result === "W" ? "bg-win" : result === "D" ? "bg-draw" : "bg-loss"
          }`}
          key={`${result}-${index}`}
          title={labels[result]}
        />
      ))}
    </div>
  );
}
