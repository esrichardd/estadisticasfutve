import { Skeleton } from "@/components/ui/skeleton";
import { getHomeStandings } from "../../api/get-home-standings";
import { StandingsTable } from "./standings-table";

type HomeStandingsLabels = {
  title: string;
  round: string;
  classification: string;
  relegation: string;
  winShort: string;
  drawShort: string;
  lossShort: string;
  tableUnavailable: string;
  recentForm: string;
  columns: {
    team: string;
    played: string;
    won: string;
    drawn: string;
    lost: string;
    goalsFor: string;
    goalsAgainst: string;
    goalDifference: string;
    form: string;
    points: string;
  };
  form: {
    W: string;
    D: string;
    L: string;
  };
};

type HomeStandingsProps =
  | { skeleton: true }
  | { skeleton?: false; labels: HomeStandingsLabels };

export async function HomeStandings(props: HomeStandingsProps) {
  if (props.skeleton) {
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
  const { labels } = props;

  return (
    <section className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-3 py-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
          {labels.title}
        </h2>
        <span className="text-[10px] text-muted-foreground">
          {labels.round}
        </span>
      </div>

      <StandingsTable
        columns={labels.columns}
        formLabels={labels.form}
        recentFormLabel={labels.recentForm}
        rows={standings.rows}
        tableUnavailableLabel={labels.tableUnavailable}
      />

      <div className="flex items-center gap-4 border-t border-border px-3 py-2">
        <div className="flex items-center gap-1.5">
          <span className="h-3 w-0.5 rounded-full bg-win" />
          <span className="text-[10px] text-muted-foreground">
            {labels.classification}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="h-3 w-0.5 rounded-full bg-loss" />
          <span className="text-[10px] text-muted-foreground">
            {labels.relegation}
          </span>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-win" /> {labels.winShort}
          </span>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-draw" />{" "}
            {labels.drawShort}
          </span>
          <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-loss" />{" "}
            {labels.lossShort}
          </span>
        </div>
      </div>
    </section>
  );
}
