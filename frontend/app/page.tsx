import { Suspense } from "react";
import { HomeHighlights } from "@/features/home/components/highlights/home-highlights";
import { HomeLeaders } from "@/features/home/components/leaders/home-leaders";
import { HomeRounds } from "@/features/home/components/rounds/home-rounds";
import { HomeSummary } from "@/features/home/components/summary/home-summary";
import { HomeShell } from "@/features/home/components/home-shell";
import { HomeStandings } from "@/features/home/components/standings/home-standings";

export default function Page() {
  return (
    <HomeShell>
      <Suspense fallback={<HomeSummary skeleton />}>
        <HomeSummary />
      </Suspense>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_340px]">
        <Suspense fallback={<HomeStandings skeleton />}>
          <HomeStandings />
        </Suspense>

        <Suspense fallback={<HomeRounds skeleton />}>
          <HomeRounds />
        </Suspense>
      </section>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Suspense fallback={<HomeLeaders skeleton />}>
          <HomeLeaders />
        </Suspense>
      </section>

      <Suspense fallback={<HomeHighlights skeleton />}>
        <HomeHighlights />
      </Suspense>
    </HomeShell>
  );
}
