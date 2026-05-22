import type { TeamSummary } from "../types/shared";

type TeamLogoProps = {
  team: TeamSummary;
  size?: "xs" | "sm" | "md";
};

const sizeClass = {
  xs: "h-5 w-5 text-[8px]",
  sm: "h-6 w-6 text-[9px]",
  md: "h-9 w-9 text-xs",
};

export function TeamLogo({ team, size = "md" }: TeamLogoProps) {
  return (
    <div
      className={`${sizeClass[size]} flex shrink-0 items-center justify-center rounded-sm border font-black`}
      style={{
        backgroundColor: `${team.color}33`,
        borderColor: `${team.color}55`,
        color: team.color,
      }}
    >
      {team.abbreviation}
    </div>
  );
}
