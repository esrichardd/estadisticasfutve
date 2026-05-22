import { Shield, Swords, TrendingUp } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { getHomeHighlights } from "../../api/get-home-highlights";
import { TeamHighlightCard } from "./team-highlight-card";

type HomeHighlightsLabels = {
  title: string;
  bestAttack: string;
  bestDefense: string;
  bestGoalDifference: string;
  goals: string;
  conceded: string;
  goalDifference: string;
};

type HomeHighlightsProps =
  | { skeleton: true }
  | { skeleton?: false; labels: HomeHighlightsLabels };

export async function HomeHighlights(props: HomeHighlightsProps) {
  if (props.skeleton) {
    return (
      <section className="overflow-hidden rounded-sm border border-border bg-card p-3">
        <div className="mb-3">
          <Skeleton className="h-4 w-48" />
        </div>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          {Array.from({ length: 3 }).map((_, index) => (
            <Skeleton className="h-28 w-full" key={index} />
          ))}
        </div>
      </section>
    );
  }

  const highlights = await getHomeHighlights();
  const { labels } = props;

  return (
    <section className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="border-b border-border px-3 py-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
          {labels.title}
        </h2>
      </div>

      <div className="grid grid-cols-1 divide-y divide-border sm:grid-cols-3 sm:divide-x sm:divide-y-0">
        {highlights.bestAttack ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<Swords size={14} />}
              label={labels.bestAttack}
              team={highlights.bestAttack.team}
              value={String(highlights.bestAttack.goalsFor)}
              valueLabel={labels.goals}
            />
          </div>
        ) : null}
        {highlights.bestDefense ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<Shield size={14} />}
              label={labels.bestDefense}
              team={highlights.bestDefense.team}
              value={String(highlights.bestDefense.goalsAgainst)}
              valueLabel={labels.conceded}
            />
          </div>
        ) : null}
        {highlights.bestGoalDifference ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<TrendingUp size={14} />}
              label={labels.bestGoalDifference}
              team={highlights.bestGoalDifference.team}
              value={`+${highlights.bestGoalDifference.goalDifference}`}
              valueLabel={labels.goalDifference}
            />
          </div>
        ) : null}
      </div>
    </section>
  );
}
