import { Shield, Swords, TrendingUp } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { getHomeHighlights } from "../../api/get-home-highlights";
import { TeamHighlightCard } from "./team-highlight-card";

type HomeHighlightsProps = { skeleton: true } | { skeleton?: false };

export async function HomeHighlights({
  skeleton = false,
}: HomeHighlightsProps) {
  if (skeleton) {
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

  return (
    <section className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="border-b border-border px-3 py-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
          Destacados por Equipo
        </h2>
      </div>

      <div className="grid grid-cols-1 divide-y divide-border sm:grid-cols-3 sm:divide-x sm:divide-y-0">
        {highlights.bestAttack ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<Swords size={14} />}
              label="Mejor Ataque"
              team={highlights.bestAttack.team}
              value={String(highlights.bestAttack.goalsFor)}
              valueLabel="goles"
            />
          </div>
        ) : null}
        {highlights.bestDefense ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<Shield size={14} />}
              label="Mejor Defensa"
              team={highlights.bestDefense.team}
              value={String(highlights.bestDefense.goalsAgainst)}
              valueLabel="recibidos"
            />
          </div>
        ) : null}
        {highlights.bestGoalDifference ? (
          <div className="p-3">
            <TeamHighlightCard
              icon={<TrendingUp size={14} />}
              label="Mayor Diferencia"
              team={highlights.bestGoalDifference.team}
              value={`+${highlights.bestGoalDifference.goalDifference}`}
              valueLabel="dif. goles"
            />
          </div>
        ) : null}
      </div>
    </section>
  );
}
