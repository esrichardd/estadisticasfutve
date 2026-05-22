import { Crosshair, Share2 } from "lucide-react";
import { TeamLogo } from "../team-logo";
import type { PlayerLeader } from "../../types/leaders";
import { PlayerLeaderRow } from "./player-leader-row";

type LeaderboardCardProps = {
  title: string;
  statLabel: string;
  topStatLabel: string;
  roundLabel: string;
  emptyLabel: string;
  leaders: PlayerLeader[];
  type: "scorers" | "assisters";
};

export function LeaderboardCard({
  title,
  statLabel,
  topStatLabel,
  roundLabel,
  emptyLabel,
  leaders,
  type,
}: LeaderboardCardProps) {
  const isScorers = type === "scorers";
  const [topLeader, ...rest] = leaders;

  return (
    <article className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-3 py-2">
        <div className="flex items-center gap-1.5">
          {isScorers ? (
            <Crosshair className="text-secondary" size={12} />
          ) : (
            <Share2 className="text-secondary" size={12} />
          )}
          <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
            {title}
          </h2>
        </div>
        <span className="text-[10px] text-muted-foreground">{roundLabel}</span>
      </div>

      {topLeader ? (
        <div
          className="flex items-center gap-3 border-b border-border px-3 py-3"
          style={{
            background: `linear-gradient(135deg, ${topLeader.team.color}18 0%, transparent 60%)`,
          }}
        >
          <div className="flex w-6 shrink-0 flex-col items-center justify-center">
            <span className="text-lg font-black leading-none text-secondary">
              1
            </span>
          </div>
          <TeamLogo size="md" team={topLeader.team} />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-bold text-foreground">
              {topLeader.player.name}
            </p>
            <p className="text-[11px] text-muted-foreground">
              {topLeader.team.shortName}
            </p>
          </div>
          <div className="shrink-0 text-right">
            <span className="text-xl font-black leading-none text-secondary">
              {topLeader.value}
            </span>
            <p className="text-[10px] text-muted-foreground">
              {topStatLabel}
            </p>
          </div>
        </div>
      ) : null}

      {rest.length ? (
        <ol>
          {rest.map((leader, index) => (
            <PlayerLeaderRow
              index={index + 1}
              key={leader.player.id}
              leader={leader}
              statLabel={statLabel}
            />
          ))}
        </ol>
      ) : (
        <p className="px-3 py-4 text-xs text-muted-foreground">
          {emptyLabel}
        </p>
      )}
    </article>
  );
}
