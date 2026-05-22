import type { FormResult, TeamSummary } from "./shared";

export type HomeStandingRow = {
  position: number;
  team: TeamSummary;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  goalsFor: number;
  goalsAgainst: number;
  goalDifference: number;
  points: number;
  form: FormResult[];
};

export type HomeStandingsResponse = {
  phaseId: string;
  groupId: string | null;
  rows: HomeStandingRow[];
};
