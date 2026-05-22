"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Locale } from "@/lib/i18n/config";

type LanguageSwitcherProps = {
  locale: Locale;
  label: string;
};

export function LanguageSwitcher({ label, locale }: LanguageSwitcherProps) {
  const pathname = usePathname();
  const nextLocale: Locale = locale === "es" ? "en" : "es";
  const flag = locale === "es" ? "🇺🇸" : "🇪🇸";
  const code = locale === "es" ? "EN" : "ES";
  const href = pathname.startsWith(`/${locale}`)
    ? pathname.replace(`/${locale}`, `/${nextLocale}`)
    : `/${nextLocale}`;

  return (
    <Link
      aria-label={label}
      className="flex h-8 shrink-0 items-center gap-1.5 rounded-sm border border-border bg-accent px-2 text-xs font-bold text-foreground transition-colors hover:border-secondary hover:bg-secondary/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary"
      href={href}
      title={label}
    >
      <span aria-hidden="true" className="text-sm">
        {flag}
      </span>
      <span>{code}</span>
    </Link>
  );
}
