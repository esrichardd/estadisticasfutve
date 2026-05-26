import { Trophy } from "lucide-react";
import type { HomeStandingsResponse } from "../../types/standings";

type BracketStandings = Extract<HomeStandingsResponse, { viewType: "bracket" }>;

type StandingsBracketProps = {
  standings: BracketStandings;
  labels: {
    matchTitle: string;
    leaderA: string;
    leaderB: string;
    tbd: string;
    annotation: string;
  };
};

function FinalistSlot({
  fallbackLabel,
  fromGroupName,
  teamName,
}: {
  fallbackLabel: string;
  fromGroupName?: string;
  teamName?: string;
}) {
  return (
    <div className="flex min-h-20 flex-1 flex-col justify-center rounded-sm border border-border bg-accent/60 px-3 py-2">
      <span className="mb-1 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
        {fromGroupName ?? fallbackLabel}
      </span>
      <span className="text-sm font-black text-foreground">
        {teamName ?? fallbackLabel}
      </span>
    </div>
  );
}

export function StandingsBracket({ labels, standings }: StandingsBracketProps) {
  return (
    <div className="px-3 py-4">
      <div className="mb-3 flex items-center gap-2 text-secondary">
        <Trophy size={16} />
        <h3 className="text-xs font-bold uppercase tracking-widest">
          {labels.matchTitle}
        </h3>
      </div>

      <div className="flex flex-col items-stretch gap-3 sm:flex-row sm:items-center">
        <FinalistSlot
          fallbackLabel={labels.leaderA}
          fromGroupName={standings.finalist?.fromGroupName}
          teamName={standings.finalist?.teamName}
        />
        <div className="self-center text-xs font-black text-muted-foreground">
          VS
        </div>
        <FinalistSlot
          fallbackLabel={standings.opponent ? labels.leaderB : labels.tbd}
          fromGroupName={standings.opponent?.fromGroupName}
          teamName={standings.opponent?.teamName}
        />
      </div>

      {!standings.finalist || !standings.opponent ? (
        <p className="mt-3 text-xs text-muted-foreground">
          {labels.annotation}
        </p>
      ) : null}
    </div>
  );
}
