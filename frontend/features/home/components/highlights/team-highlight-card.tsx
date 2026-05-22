import { TeamLogo } from "../team-logo";
import type { TeamSummary } from "../../types/shared";

type TeamHighlightCardProps = {
  label: string;
  icon: React.ReactNode;
  team: TeamSummary;
  value: string;
  valueLabel: string;
};

export function TeamHighlightCard({
  label,
  icon,
  team,
  value,
  valueLabel,
}: TeamHighlightCardProps) {
  return (
    <article className="flex items-center gap-3 rounded-sm border border-border bg-card px-3 py-3 transition-colors hover:border-primary/30">
      <div className="shrink-0 text-secondary">{icon}</div>
      <div className="min-w-0 flex-1">
        <p className="mb-1 text-[10px] font-medium uppercase tracking-widest text-muted-foreground">
          {label}
        </p>
        <div className="flex items-center gap-2">
          <TeamLogo team={team} size="sm" />
          <span className="truncate text-sm font-bold text-foreground">
            {team.shortName}
          </span>
        </div>
      </div>
      <div className="shrink-0 text-right">
        <span className="text-lg font-black leading-none text-secondary">
          {value}
        </span>
        <p className="text-[10px] text-muted-foreground">{valueLabel}</p>
      </div>
    </article>
  );
}
