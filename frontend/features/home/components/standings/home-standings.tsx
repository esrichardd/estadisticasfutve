import { Skeleton } from "@/components/ui/skeleton";
import { getHomeStandings } from "../../api/get-home-standings";
import { StandingsTable } from "./standings-table";

type HomeStandingsProps = { skeleton: true } | { skeleton?: false };

export async function HomeStandings({ skeleton = false }: HomeStandingsProps) {
  if (skeleton) {
    return (
      <section className="overflow-hidden rounded-sm border border-border bg-card p-3">
        <div className="mb-3 flex items-center justify-between">
          <Skeleton className="h-4 w-44" />
          <Skeleton className="h-3 w-16" />
        </div>
        <div className="skeleton-table">
          {Array.from({ length: 12 }).map((_, index) => (
            <Skeleton className="h-9 w-full" key={index} />
          ))}
        </div>
      </section>
    );
  }

  const standings = await getHomeStandings();

  return (
    <section className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-3 py-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
          Tabla de Posiciones
        </h2>
        <span className="text-[10px] text-muted-foreground">Jornada 8</span>
      </div>

      <StandingsTable rows={standings.rows} />

      <div className="flex items-center gap-4 border-t border-border px-3 py-2">
        <div className="flex items-center gap-1.5">
          <span className="h-3 w-0.5 rounded-full bg-win" />
          <span className="text-[10px] text-muted-foreground">
            Clasificación
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="h-3 w-0.5 rounded-full bg-loss" />
          <span className="text-[10px] text-muted-foreground">Descenso</span>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-win" /> V
          </span>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-draw" /> E
          </span>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-loss" /> D
          </span>
        </div>
      </div>
    </section>
  );
}
