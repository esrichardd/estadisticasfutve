import { localeFormats, type Locale } from "./config";

export function getFormatLocale(locale: Locale) {
  return localeFormats[locale];
}
