import { Skeleton } from "@/components/ui/skeleton";
import { getHomePhasesResponse } from "../../api/get-home-phases";
import { getHomeStandings } from "../../api/get-home-standings";
import type {
  HomePhaseType,
  HomeStandingHighlight,
} from "../../types/standings";
import { PhaseTabs } from "./phase-tabs";
import { StandingsBracket } from "./standings-bracket";
import { StandingsTable } from "./standings-table";

type HomeStandingsLabels = {
  title: string;
  round: string;
  winShort: string;
  drawShort: string;
  lossShort: string;
  tableUnavailable: string;
  recentForm: string;
  phases: {
    current: string;
    names: Record<HomePhaseType, string>;
  };
  bracket: {
    matchTitle: string;
    leaderA: string;
    leaderB: string;
    tbd: string;
    annotation: string;
  };
  legend: Record<HomeStandingHighlight["key"], string>;
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
  | {
      skeleton?: false;
      labels: HomeStandingsLabels;
      phaseParam?: string;
    };

function getPhaseLabel(
  phaseType: HomePhaseType | undefined,
  labels: HomeStandingsLabels,
) {
  return phaseType ? labels.phases.names[phaseType] : labels.round;
}

function StandingsLegend({
  highlights,
  labels,
}: {
  highlights: HomeStandingHighlight[];
  labels: HomeStandingsLabels;
}) {
  return (
    <div className="flex flex-wrap items-center gap-4 border-t border-border px-3 py-2">
      {highlights.map((highlight) => (
        <div className="flex items-center gap-1.5" key={highlight.key}>
          <span
            className={`h-3 w-0.5 rounded-full ${
              highlight.tone === "promotion" ? "bg-win" : "bg-loss"
            }`}
          />
          <span className="text-[10px] text-muted-foreground">
            {labels.legend[highlight.key]}
          </span>
        </div>
      ))}

      <div className="ml-auto flex items-center gap-4">
        <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
          <span className="h-2 w-2 rounded-full bg-win" /> {labels.winShort}
        </span>
        <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
          <span className="h-2 w-2 rounded-full bg-draw" /> {labels.drawShort}
        </span>
        <span className="flex items-center gap-1 text-[10px] text-muted-foreground">
          <span className="h-2 w-2 rounded-full bg-loss" /> {labels.lossShort}
        </span>
      </div>
    </div>
  );
}

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

  const [standings, phasesResponse] = await Promise.all([
    getHomeStandings(props.phaseParam),
    getHomePhasesResponse(),
  ]);
  const { labels } = props;
  const activeParam = phasesResponse.phases.some(
    (phase) => phase.id === props.phaseParam,
  )
    ? (props.phaseParam ?? null)
    : null;
  const selectedPhase = phasesResponse.phases.find(
    (phase) => phase.id === standings.phaseId,
  );
  const phaseLabel = getPhaseLabel(selectedPhase?.type, labels);

  return (
    <section className="overflow-hidden rounded-sm border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-3 py-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-foreground">
          {labels.title}
        </h2>
        <span className="text-[10px] text-muted-foreground">{phaseLabel}</span>
      </div>

      <PhaseTabs
        activeParam={activeParam}
        labels={labels.phases}
        phases={phasesResponse.phases}
      />

      {standings.viewType === "single_table" ? (
        <>
          <StandingsTable
            columns={labels.columns}
            formLabels={labels.form}
            highlights={standings.highlights}
            recentFormLabel={labels.recentForm}
            rows={standings.rows}
            tableUnavailableLabel={labels.tableUnavailable}
          />
          <StandingsLegend highlights={standings.highlights} labels={labels} />
        </>
      ) : null}

      {standings.viewType === "grouped_tables" ? (
        <>
          <div className="flex flex-col">
            {standings.groups.map((group) => (
              <div
                className="border-b border-border last:border-b-0"
                key={group.id}
              >
                <h3 className="border-b border-border/60 px-3 py-2 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                  {group.name}
                </h3>
                <StandingsTable
                  columns={labels.columns}
                  formLabels={labels.form}
                  highlights={standings.highlights}
                  recentFormLabel={labels.recentForm}
                  rows={group.rows}
                  tableUnavailableLabel={labels.tableUnavailable}
                />
              </div>
            ))}
          </div>
          <StandingsLegend highlights={standings.highlights} labels={labels} />
        </>
      ) : null}

      {standings.viewType === "bracket" ? (
        <StandingsBracket labels={labels.bracket} standings={standings} />
      ) : null}
    </section>
  );
}
