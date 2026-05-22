import { Calendar, Crosshair, Trophy, Zap } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { getHomeSummary } from "../../api/get-home-summary";
import { formatLastUpdated } from "../../utils/format-date";

type HomeSummaryLabels = {
  updated: string;
  notUpdated: string;
  leader: string;
  totalGoals: string;
  matches: string;
  next: string;
  pointsAbbr: string;
  playedMatches: string;
  played: string;
  nextMatchTime: string;
};

type HomeSummaryProps =
  | { skeleton: true }
  | { skeleton?: false; labels: HomeSummaryLabels; formatLocale: string };

type MetricCardProps = {
  icon: React.ReactNode;
  label: string;
  value: string;
  sub?: string;
};

function MetricCard({ icon, label, value, sub }: MetricCardProps) {
  return (
    <div className="flex min-w-0 items-center gap-3 rounded-sm border border-border bg-accent/60 px-3 py-2">
      <div className="shrink-0 text-secondary">{icon}</div>
      <div className="min-w-0">
        <p className="mb-1 text-[10px] font-medium uppercase leading-none tracking-widest text-muted-foreground">
          {label}
        </p>
        <p className="truncate text-sm font-bold text-foreground">{value}</p>
        {sub ? (
          <p className="mt-0.5 text-[10px] text-muted-foreground">{sub}</p>
        ) : null}
      </div>
    </div>
  );
}

export async function HomeSummary(props: HomeSummaryProps) {
  if (props.skeleton) {
    return (
      <section className="border-b border-border bg-card">
        <div className="mx-auto max-w-[1400px] px-0 py-0">
          <Skeleton className="h-3 w-32" />
          <Skeleton className="mt-3 h-9 w-64" />
          <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <Skeleton className="h-14 w-full" key={index} />
            ))}
          </div>
        </div>
      </section>
    );
  }

  const summary = await getHomeSummary();
  const { formatLocale, labels } = props;

  return (
    <section className="border-b border-border bg-card">
      <div className="mx-auto max-w-[1400px] px-0 py-0">
        <div className="mb-3 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-bold text-secondary">
              {summary.league.name} {summary.season.displayName}{" "}
              {summary.tournament.name}
            </span>
            <span className="text-border">·</span>
            <span className="text-xs text-muted-foreground">
              {summary.phase.name}
            </span>
            <span className="text-border">·</span>
            <span className="text-xs font-semibold text-muted-foreground">
              {summary.currentRound?.name}
            </span>
          </div>
          <span className="text-[11px] text-muted-foreground">
            {labels.updated}{" "}
            {formatLastUpdated(
              summary.lastUpdated,
              formatLocale,
              labels.notUpdated,
            )}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          <MetricCard
            icon={<Trophy size={14} />}
            label={labels.leader}
            sub={`${summary.metrics.leader.points} ${labels.pointsAbbr}`}
            value={summary.metrics.leader.teamName}
          />
          <MetricCard
            icon={<Crosshair size={14} />}
            label={labels.totalGoals}
            sub={`${summary.metrics.playedMatches} ${labels.playedMatches}`}
            value={String(summary.metrics.totalGoals)}
          />
          <MetricCard
            icon={<Calendar size={14} />}
            label={labels.matches}
            sub={summary.currentRound?.name}
            value={`${summary.metrics.playedMatches} ${labels.played}`}
          />
          <MetricCard
            icon={<Zap size={14} />}
            label={labels.next}
            sub={labels.nextMatchTime}
            value={summary.metrics.nextMatch}
          />
        </div>
      </div>
    </section>
  );
}
