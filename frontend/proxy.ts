import { NextResponse, type NextRequest } from "next/server";
import { defaultLocale, isLocale, locales } from "@/lib/i18n/config";

function getPreferredLocale(request: NextRequest) {
  const cookieLocale = request.cookies.get("NEXT_LOCALE")?.value;

  if (isLocale(cookieLocale)) {
    return cookieLocale;
  }

  const acceptedLanguages = request.headers
    .get("accept-language")
    ?.split(",")
    .map((language) => language.split(";")[0]?.trim().toLowerCase())
    .filter(Boolean);

  for (const acceptedLanguage of acceptedLanguages ?? []) {
    if (isLocale(acceptedLanguage)) {
      return acceptedLanguage;
    }

    const baseLanguage = acceptedLanguage.split("-")[0];

    if (isLocale(baseLanguage)) {
      return baseLanguage;
    }
  }

  return defaultLocale;
}

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const pathnameHasLocale = locales.some(
    (locale) => pathname === `/${locale}` || pathname.startsWith(`/${locale}/`),
  );

  if (pathnameHasLocale) {
    return NextResponse.next();
  }

  const url = request.nextUrl.clone();
  const locale = getPreferredLocale(request);
  url.pathname = `/${locale}${pathname === "/" ? "" : pathname}`;

  return NextResponse.redirect(url);
}

export const config = {
  matcher: ["/((?!api|_next|.*\\..*).*)"],
};
