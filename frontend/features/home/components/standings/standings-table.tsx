import type { HomeStandingRow } from "../../types/standings";
import { StandingsRow } from "./standings-row";

type StandingsTableProps = {
  rows: HomeStandingRow[];
};

export function StandingsTable({ rows }: StandingsTableProps) {
  if (rows.length === 0) {
    return (
      <p className="px-3 py-6 text-xs text-muted-foreground">
        Tabla no disponible para esta fase.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="standings-table w-full text-xs">
        <thead>
          <tr className="border-b border-border text-muted-foreground">
            <th className="w-7 px-2 py-1.5 text-left font-medium">#</th>
            <th className="px-2 py-1.5 text-left font-medium">Equipo</th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">PJ</th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">G</th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">E</th>
            <th className="w-7 px-1.5 py-1.5 text-center font-medium">P</th>
            <th className="w-8 px-1.5 py-1.5 text-center font-medium">GF</th>
            <th className="w-8 px-1.5 py-1.5 text-center font-medium">GC</th>
            <th className="w-8 px-1.5 py-1.5 text-center font-medium">DG</th>
            <th className="w-16 whitespace-nowrap px-1.5 py-1.5 text-center font-medium">
              Forma
            </th>
            <th className="w-10 px-2 py-1.5 text-center font-bold text-secondary">
              PTS
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <StandingsRow key={row.team.id} row={row} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
