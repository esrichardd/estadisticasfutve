export function formatShortDateTime(value: string) {
  return new Intl.DateTimeFormat("es-VE", {
    day: "2-digit",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatLastUpdated(value: string | null) {
  if (!value) return "Sin actualizar";

  return new Intl.DateTimeFormat("es-VE", {
    day: "2-digit",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}
