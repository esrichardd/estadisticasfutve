import type { FormResult } from "../../types/shared";

type FormIndicatorProps = {
  form: FormResult[];
};

const label = {
  W: "Victoria",
  D: "Empate",
  L: "Derrota",
};

export function FormIndicator({ form }: FormIndicatorProps) {
  return (
    <div
      className="flex items-center justify-center gap-0.5"
      aria-label="Forma reciente"
    >
      {form.map((result, index) => (
        <span
          aria-label={label[result]}
          className={`inline-block h-2 w-2 rounded-full ${
            result === "W" ? "bg-win" : result === "D" ? "bg-draw" : "bg-loss"
          }`}
          key={`${result}-${index}`}
          title={label[result]}
        />
      ))}
    </div>
  );
}
