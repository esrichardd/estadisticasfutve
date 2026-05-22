export const locales = ["es", "en"] as const;

export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "es";

export const localeFormats: Record<Locale, string> = {
  es: "es-VE",
  en: "en-US",
};

export function isLocale(value: string | undefined): value is Locale {
  return locales.includes(value as Locale);
}
