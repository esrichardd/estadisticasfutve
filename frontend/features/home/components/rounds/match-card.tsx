import { TeamLogo } from "../team-logo";
import type { HomeMatch } from "../../types/rounds";
import { formatShortTime } from "../../utils/format-date";

type MatchCardProps = {
  match: HomeMatch;
  formatLocale: string;
  labels: {
    finished: string;
    scheduledShort: string;
  };
};

function StatusBadge({
  labels,
  match,
}: {
  labels: MatchCardProps["labels"];
  match: HomeMatch;
}) {
  if (match.status === "live") {
    return (
      <div className="flex items-center gap-1 rounded-sm border border-win/30 bg-win/10 px-1.5 py-0.5">
        <span className="live-dot h-1.5 w-1.5 rounded-full bg-win" />
        <span className="text-[10px] font-bold text-win">
          {match.liveMinute ?? "-"}&apos;
        </span>
      </div>
    );
  }

  if (match.status === "finished") {
    return (
      <div className="rounded-sm border border-border bg-muted px-1.5 py-0.5">
        <span className="text-[10px] font-medium text-muted-foreground">
          {labels.finished}
        </span>
      </div>
    );
  }

  return (
    <div className="rounded-sm border border-primary/20 bg-primary/10 px-1.5 py-0.5">
      <span className="text-[10px] font-medium text-primary-foreground/70">
        {labels.scheduledShort}
      </span>
    </div>
  );
}

export function MatchCard({ formatLocale, labels, match }: MatchCardProps) {
  const isLive = match.status === "live";
  const hasScore = match.homeScore !== null && match.awayScore !== null;
  const kickoff = formatShortTime(match.scheduledDatetime, formatLocale);

  return (
    <article
      className={`flex items-center gap-2 border-b border-border/50 px-3 py-2 last:border-0 ${
        isLive ? "bg-win/5" : "hover:bg-accent/30"
      } transition-colors`}
    >
      <div className="flex min-w-0 flex-1 items-center justify-end gap-1.5">
        <span
          className={`truncate text-right text-xs font-semibold ${
            isLive ? "text-foreground" : "text-foreground/80"
          }`}
        >
          {match.homeTeam.shortName}
        </span>
        <TeamLogo team={match.homeTeam} size="xs" />
      </div>

      <div className="flex w-20 shrink-0 flex-col items-center gap-0.5">
        {hasScore ? (
          <div className="flex items-center gap-1">
            <span
              className={`text-sm font-black ${
                isLive ? "text-win" : "text-foreground"
              }`}
            >
              {match.homeScore}
            </span>
            <span className="text-xs text-muted-foreground">-</span>
            <span
              className={`text-sm font-black ${
                isLive ? "text-win" : "text-foreground"
              }`}
            >
              {match.awayScore}
            </span>
          </div>
        ) : (
          <span className="text-xs font-bold text-secondary">{kickoff}</span>
        )}
        <StatusBadge labels={labels} match={match} />
      </div>

      <div className="flex min-w-0 flex-1 items-center justify-start gap-1.5">
        <TeamLogo team={match.awayTeam} size="xs" />
        <span
          className={`truncate text-xs font-semibold ${
            isLive ? "text-foreground" : "text-foreground/80"
          }`}
        >
          {match.awayTeam.shortName}
        </span>
      </div>
    </article>
  );
}
