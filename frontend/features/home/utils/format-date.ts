export function formatShortDateTime(value: string, formatLocale: string) {
  return new Intl.DateTimeFormat(formatLocale, {
    day: "2-digit",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatShortTime(value: string, formatLocale: string) {
  return new Intl.DateTimeFormat(formatLocale, {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function formatLastUpdated(
  value: string | null,
  formatLocale: string,
  emptyLabel: string,
) {
  if (!value) return emptyLabel;

  return new Intl.DateTimeFormat(formatLocale, {
    day: "2-digit",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}
