"use client";

import { useState } from "react";
import type { HomeRound, HomeRoundsResponse } from "../../types/rounds";
import { MatchCard } from "./match-card";

type RoundsLabels = {
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

type RoundsTabsProps = {
  rounds: HomeRoundsResponse;
  formatLocale: string;
  labels: RoundsLabels;
};

// ── Subcomponente: lista de partidos de un round ──────────────────────────────

function RoundMatchList({
  formatLocale,
  labels,
  round,
  emptyLabel,
}: {
  round: HomeRound | null | undefined;
  formatLocale: string;
  labels: RoundsLabels["status"];
  emptyLabel: string;
}) {
  if (!round?.matches.length) {
    return (
      <p className="px-3 py-6 text-center text-xs text-muted-foreground">
        {emptyLabel}
      </p>
    );
  }
  return (
    <>
      {round.matches.map((match) => (
        <MatchCard
          formatLocale={formatLocale}
          key={match.id}
          labels={labels}
          match={match}
        />
      ))}
    </>
  );
}

// ── Modo grouped: muestra cada grupo como sección ────────────────────────────

function GroupedRounds({
  formatLocale,
  groups,
  labels,
  tab,
}: {
  groups: NonNullable<Extract<HomeRoundsResponse, { mode: "grouped" }>["groups"]>;
  tab: "latest" | "next";
  formatLocale: string;
  labels: RoundsLabels;
}) {
  return (
    <div className="flex flex-col">
      {groups.map((group, idx) => {
        const round = tab === "latest" ? group.latest : group.next;
        return (
          <div
            className={idx < groups.length - 1 ? "border-b border-border" : ""}
            key={group.groupId}
          >
            <p className="border-b border-border/60 px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
              {group.groupName}
            </p>
            <RoundMatchList
              emptyLabel={labels.empty}
              formatLocale={formatLocale}
              labels={labels.status}
              round={round}
            />
          </div>
        );
      })}
    </div>
  );
}

// ── Componente principal ──────────────────────────────────────────────────────

export function RoundsTabs({ formatLocale, labels, rounds }: RoundsTabsProps) {
  const [tab, setTab] = useState<"latest" | "next">("latest");

  // Calcular partidos en vivo según el modo
  const liveMatches =
    rounds.mode === "single"
      ? (tab === "latest" ? rounds.latest : rounds.next)?.matches.filter(
          (m) => m.status === "live",
        ).length ?? 0
      : rounds.groups
          .flatMap((g) => (tab === "latest" ? g.latest : g.next)?.matches ?? [])
          .filter((m) => m.status === "live").length;

  // Label del tab latest: muestra número de jornada solo en modo single
  const latestNumber =
    rounds.mode === "single" ? (rounds.latest?.number ?? "-") : null;
  const nextNumber =
    rounds.mode === "single" ? (rounds.next?.number ?? "-") : null;

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
          {latestNumber !== null
            ? `${labels.latestRound} (${labels.roundShort}${latestNumber})`
            : labels.latestRound}
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
          {nextNumber !== null
            ? `${labels.round} ${nextNumber}`
            : labels.round}
        </button>
      </div>

      <div className="flex flex-col">
        {rounds.mode === "grouped" ? (
          <GroupedRounds
            formatLocale={formatLocale}
            groups={rounds.groups}
            labels={labels}
            tab={tab}
          />
        ) : (
          <RoundMatchList
            emptyLabel={labels.empty}
            formatLocale={formatLocale}
            labels={labels.status}
            round={tab === "latest" ? rounds.latest : rounds.next}
          />
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
