import { Skeleton } from "@/components/ui/skeleton";
import { getHomeLeaders } from "../../api/get-home-leaders";
import { LeaderboardCard } from "./leaderboard-card";

type HomeLeadersLabels = {
  round: string;
  scorersTitle: string;
  assistersTitle: string;
  goals: string;
  assists: string;
  goalsShort: string;
  assistsShort: string;
  empty: string;
};

type HomeLeadersProps =
  | { skeleton: true }
  | { skeleton?: false; labels: HomeLeadersLabels };

export async function HomeLeaders(props: HomeLeadersProps) {
  if (props.skeleton) {
    return (
      <>
        {Array.from({ length: 2 }).map((_, cardIndex) => (
          <article
            className="overflow-hidden rounded-sm border border-border bg-card p-3"
            key={cardIndex}
          >
            <div className="mb-3 flex items-center justify-between">
              <Skeleton className="h-4 w-44" />
              <Skeleton className="h-3 w-16" />
            </div>
            <div className="grid gap-2">
              {Array.from({ length: 5 }).map((__, index) => (
                <Skeleton className="h-11 w-full" key={index} />
              ))}
            </div>
          </article>
        ))}
      </>
    );
  }

  const leaders = await getHomeLeaders();
  const { labels } = props;

  return (
    <>
      <LeaderboardCard
        emptyLabel={labels.empty}
        leaders={leaders.scorers}
        roundLabel={labels.round}
        statLabel={labels.goals}
        title={labels.scorersTitle}
        topStatLabel={labels.goalsShort}
        type="scorers"
      />
      <LeaderboardCard
        emptyLabel={labels.empty}
        leaders={leaders.assisters}
        roundLabel={labels.round}
        statLabel={labels.assists}
        title={labels.assistersTitle}
        topStatLabel={labels.assistsShort}
        type="assisters"
      />
    </>
  );
}
