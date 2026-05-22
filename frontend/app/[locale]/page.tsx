import { Suspense } from "react";
import { notFound } from "next/navigation";
import { HomeHighlights } from "@/features/home/components/highlights/home-highlights";
import { HomeLeaders } from "@/features/home/components/leaders/home-leaders";
import { HomeRounds } from "@/features/home/components/rounds/home-rounds";
import { HomeSummary } from "@/features/home/components/summary/home-summary";
import { HomeShell } from "@/features/home/components/home-shell";
import { HomeStandings } from "@/features/home/components/standings/home-standings";
import { getDictionary } from "@/lib/i18n/get-dictionary";
import { isLocale } from "@/lib/i18n/config";
import { getFormatLocale } from "@/lib/i18n/format";

type PageProps = {
  params: Promise<{ locale: string }>;
};

export default async function Page({ params }: PageProps) {
  const { locale } = await params;

  if (!isLocale(locale)) {
    notFound();
  }

  const dictionary = await getDictionary(locale);
  const formatLocale = getFormatLocale(locale);

  return (
    <HomeShell labels={dictionary.shell}>
      <Suspense fallback={<HomeSummary skeleton />}>
        <HomeSummary
          formatLocale={formatLocale}
          labels={dictionary.home.summary}
        />
      </Suspense>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_340px]">
        <Suspense fallback={<HomeStandings skeleton />}>
          <HomeStandings labels={dictionary.home.standings} />
        </Suspense>

        <Suspense fallback={<HomeRounds skeleton />}>
          <HomeRounds
            formatLocale={formatLocale}
            labels={dictionary.home.rounds}
          />
        </Suspense>
      </section>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Suspense fallback={<HomeLeaders skeleton />}>
          <HomeLeaders labels={dictionary.home.leaders} />
        </Suspense>
      </section>

      <Suspense fallback={<HomeHighlights skeleton />}>
        <HomeHighlights labels={dictionary.home.highlights} />
      </Suspense>
    </HomeShell>
  );
}
