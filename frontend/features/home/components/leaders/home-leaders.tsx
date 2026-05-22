import { Skeleton } from "@/components/ui/skeleton";
import { getHomeLeaders } from "../../api/get-home-leaders";
import { LeaderboardCard } from "./leaderboard-card";

type HomeLeadersProps = { skeleton: true } | { skeleton?: false };

export async function HomeLeaders({ skeleton = false }: HomeLeadersProps) {
  if (skeleton) {
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

  return (
    <>
      <LeaderboardCard
        leaders={leaders.scorers}
        statLabel="Goles"
        title="Máximos goleadores"
        type="scorers"
      />
      <LeaderboardCard
        leaders={leaders.assisters}
        statLabel="Asistencias"
        title="Máximos asistentes"
        type="assisters"
      />
    </>
  );
}
