"use client";

import { useState } from "react";
import type { HomeRound } from "../../types/rounds";
import { MatchCard } from "./match-card";

type RoundsTabsProps = {
  latest: HomeRound | null;
  next: HomeRound | null;
};

export function RoundsTabs({ latest, next }: RoundsTabsProps) {
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
          Ultima Jornada (J{latest?.number ?? "-"})
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
          Jornada {next?.number ?? "-"}
        </button>
      </div>

      <div className="flex flex-col">
        {selected?.matches.length ? (
          selected.matches.map((match) => (
            <MatchCard key={match.id} match={match} />
          ))
        ) : (
          <p className="px-3 py-6 text-center text-xs text-muted-foreground">
            No hay partidos disponibles.
          </p>
        )}
      </div>

      {tab === "next" && liveMatches > 0 ? (
        <div className="flex items-center gap-1.5 border-t border-border px-3 py-2">
          <span className="live-dot h-1.5 w-1.5 rounded-full bg-win" />
          <span className="text-[10px] text-muted-foreground">
            {liveMatches} partidos en vivo
          </span>
        </div>
      ) : null}
    </section>
  );
}
