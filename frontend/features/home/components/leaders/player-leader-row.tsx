import { TeamLogo } from "../team-logo";
import type { PlayerLeader } from "../../types/leaders";

type PlayerLeaderRowProps = {
  leader: PlayerLeader;
  index: number;
  statLabel: string;
};

export function PlayerLeaderRow({
  leader,
  index,
  statLabel,
}: PlayerLeaderRowProps) {
  return (
    <li className="flex items-center gap-2 border-b border-border/40 px-3 py-1.5 transition-colors last:border-0 hover:bg-accent/30">
      <span className="w-4 shrink-0 text-center text-[11px] font-medium text-muted-foreground">
        {index + 1}
      </span>
      <TeamLogo team={leader.team} size="xs" />
      <div className="min-w-0 flex-1">
        <p className="truncate text-[11px] font-medium text-foreground">
          {leader.player.name}
        </p>
        <p className="text-[10px] text-muted-foreground">
          {leader.team.shortName}
        </p>
      </div>
      <strong
        className="shrink-0 text-xs font-bold text-foreground"
        aria-label={statLabel}
      >
        {leader.value}
      </strong>
    </li>
  );
}
