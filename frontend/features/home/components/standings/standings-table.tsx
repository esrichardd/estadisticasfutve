import type {
  HomeStandingHighlight,
  HomeStandingRow,
} from "../../types/standings";
import { StandingsRow } from "./standings-row";

type StandingsTableProps = {
  rows: HomeStandingRow[];
  highlights: HomeStandingHighlight[];
  tableUnavailableLabel: string;
  recentFormLabel: string;
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
  formLabels: {
    W: string;
    D: string;
    L: string;
  };
};

export function StandingsTable({
  columns,
  formLabels,
  highlights,
  recentFormLabel,
  rows,
  tableUnavailableLabel,
}: StandingsTableProps) {
  if (rows.length === 0) {
    return (
      <p className="px-3 py-6 text-xs text-muted-foreground">
        {tableUnavailableLabel}
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="standings-table w-full text-xs">
        <thead>
          <tr className="border-b border-border text-muted-foreground">
            <th className="w-7 px-2 py-1.5 text-left font-medium">#</th>
            <th className="px-2 py-1.5 text-left font-medium">
              {columns.team}
            </th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">
              {columns.played}
            </th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">
              {columns.won}
            </th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">
              {columns.drawn}
            </th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">
              {columns.lost}
            </th>
            <th className="hidden w-8 px-1.5 py-1.5 text-center font-medium sm:table-cell">
              {columns.goalsFor}
            </th>
            <th className="hidden w-8 px-1.5 py-1.5 text-center font-medium sm:table-cell">
              {columns.goalsAgainst}
            </th>
            <th className="w-8 px-1.5 py-1.5 text-center font-medium">
              {columns.goalDifference}
            </th>
            <th className="w-16 whitespace-nowrap px-1.5 py-1.5 text-center font-medium">
              {columns.form}
            </th>
            <th className="w-10 px-2 py-1.5 text-center font-bold text-secondary">
              {columns.points}
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <StandingsRow
              formLabels={formLabels}
              highlights={highlights}
              key={row.team.id}
              recentFormLabel={recentFormLabel}
              row={row}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
