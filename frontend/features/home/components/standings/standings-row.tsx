import { TeamLogo } from "../team-logo";
import type { HomeStandingRow } from "../../types/standings";
import { FormIndicator } from "./form-indicator";

type StandingsRowProps = {
  row: HomeStandingRow;
  recentFormLabel: string;
  formLabels: {
    W: string;
    D: string;
    L: string;
  };
};

export function StandingsRow({
  formLabels,
  recentFormLabel,
  row,
}: StandingsRowProps) {
  const goalDifference =
    row.goalDifference > 0 ? `+${row.goalDifference}` : row.goalDifference;
  const isLeader = row.position === 1;
  const isPromotion = row.position <= 4;
  const isDanger = row.position >= 11;

  return (
    <tr
      className={`border-b border-border/50 transition-colors ${
        isLeader
          ? "bg-secondary/5 hover:bg-secondary/10"
          : "hover:bg-[oklch(0.20_0.010_15_/_0.6)]"
      }`}
    >
      <td className="px-2 py-1.5 text-center">
        <div className="relative flex items-center justify-center gap-1">
          {isLeader ? (
            <span className="absolute -ml-2.5 h-4 w-0.5 rounded-full bg-secondary" />
          ) : null}
          <span
            className={`text-xs font-bold ${
              isLeader
                ? "text-secondary"
                : isPromotion
                  ? "text-win"
                  : isDanger
                    ? "text-loss"
                    : "text-muted-foreground"
            }`}
          >
            {row.position}
          </span>
        </div>
      </td>
      <td className="px-2 py-1.5">
        <div className="flex min-w-[120px] items-center gap-2">
          <TeamLogo team={row.team} size="sm" />
          <span
            className={`whitespace-nowrap font-medium ${
              isLeader ? "text-secondary" : "text-foreground"
            }`}
          >
            {row.team.shortName}
          </span>
        </div>
      </td>
      <td className="px-1.5 py-1.5 text-center text-muted-foreground">
        {row.played}
      </td>
      <td className="px-1.5 py-1.5 text-center font-medium text-win">
        {row.won}
      </td>
      <td className="px-1.5 py-1.5 text-center text-muted-foreground">
        {row.drawn}
      </td>
      <td className="px-1.5 py-1.5 text-center font-medium text-loss">
        {row.lost}
      </td>
      <td className="px-1.5 py-1.5 text-center text-muted-foreground">
        {row.goalsFor}
      </td>
      <td className="px-1.5 py-1.5 text-center text-muted-foreground">
        {row.goalsAgainst}
      </td>
      <td
        className={`px-1.5 py-1.5 text-center font-medium ${
          row.goalDifference > 0
            ? "text-win"
            : row.goalDifference < 0
              ? "text-loss"
              : "text-muted-foreground"
        }`}
      >
        {goalDifference}
      </td>
      <td className="px-1.5 py-1.5">
        <FormIndicator
          form={row.form}
          labels={formLabels}
          recentFormLabel={recentFormLabel}
        />
      </td>
      <td className="px-2 py-1.5 text-center">
        <span
          className={`text-sm font-black ${
            isLeader ? "text-secondary" : "text-foreground"
          }`}
        >
          {row.points}
        </span>
      </td>
    </tr>
  );
}
