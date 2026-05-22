import type { TeamSummary } from "./shared";

export type HomeHighlightsResponse = {
  bestAttack: {
    team: TeamSummary;
    goalsFor: number;
  } | null;
  bestDefense: {
    team: TeamSummary;
    goalsAgainst: number;
  } | null;
  bestGoalDifference: {
    team: TeamSummary;
    goalDifference: number;
  } | null;
};
