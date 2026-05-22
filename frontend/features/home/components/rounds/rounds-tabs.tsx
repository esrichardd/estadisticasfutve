"use client";

import { useState } from "react";
import type { HomeRound } from "../../types/rounds";
import { MatchCard } from "./match-card";

type RoundsTabsProps = {
  latest: HomeRound | null;
  next: HomeRound | null;
  formatLocale: string;
  labels: {
    latestRound: string;
    roundShort: string;
    round: string;
    empty: string;
    liveMatchSingular: string;
    liveMatchPlural: string;
    status: {
      finished: string;
      scheduledShort: string;
    };
  };
};

export function RoundsTabs({
  latest,
  next,
  formatLocale,
  labels,
}: RoundsTabsProps) {
  const [tab, setTab] = useState<"latest" | "next">("latest");
  const selected = tab === "latest" ? latest : next;
  const liveMatches =
    selected?.matches.filter((match) => match.status === "live").length ?? 0;

  return (
    <section className="flex flex-col overflow-hidden rounded-sm border border-border bg-card">
      <div className="flex border-b border-border">
        <button
          className={`flex-1 px-3 py-2 text-xs font-semibold transition-colors ${
            tab === "latest"
              ? "border-b-2 border-secondary bg-secondary/5 text-secondary"
              : "text-muted-foreground hover:text-foreground"
          }`}
          onClick={() => setTab("latest")}
          type="button"
        >
          {labels.latestRound} ({labels.roundShort}
          {latest?.number ?? "-"})
        </button>
        <button
          className={`flex-1 px-3 py-2 text-xs font-semibold transition-colors ${
            tab === "next"
              ? "border-b-2 border-secondary bg-secondary/5 text-secondary"
              : "text-muted-foreground hover:text-foreground"
          }`}
          onClick={() => setTab("next")}
          type="button"
        >
          {labels.round} {next?.number ?? "-"}
        </button>
      </div>

      <div className="flex flex-col">
        {selected?.matches.length ? (
          selected.matches.map((match) => (
            <MatchCard
              formatLocale={formatLocale}
              key={match.id}
              labels={labels.status}
              match={match}
            />
          ))
        ) : (
          <p className="px-3 py-6 text-center text-xs text-muted-foreground">
            {labels.empty}
          </p>
        )}
      </div>

      {tab === "next" && liveMatches > 0 ? (
        <div className="flex items-center gap-1.5 border-t border-border px-3 py-2">
          <span className="live-dot h-1.5 w-1.5 rounded-full bg-win" />
          <span className="text-[10px] text-muted-foreground">
            {liveMatches}{" "}
            {liveMatches === 1
              ? labels.liveMatchSingular
              : labels.liveMatchPlural}
          </span>
        </div>
      ) : null}
    </section>
  );
}
