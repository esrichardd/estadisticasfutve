import type { FormResult, TeamSummary } from "./shared";

export type HomePhaseType =
  | "round_robin"
  | "group_stage"
  | "knockout"
  | "two_legged";

export type HomePhase = {
  id: string;
  name: string;
  type: HomePhaseType;
  isCurrent: boolean;
};

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

export type HomeStandingHighlight = {
  key: "qualifiesKnockout" | "qualifiesFinal" | "relegation";
  tone: "promotion" | "danger";
  from: number;
  to?: number;
};

export type HomeStandingsGroup = {
  id: string;
  name: string;
  rows: HomeStandingRow[];
};

type HomeStandingsBase = {
  phaseId: string;
  groupId: null;
  highlights: HomeStandingHighlight[];
};

export type HomeStandingsResponse =
  | (HomeStandingsBase & {
      viewType: "single_table";
      rows: HomeStandingRow[];
    })
  | (HomeStandingsBase & {
      viewType: "grouped_tables";
      groups: HomeStandingsGroup[];
    })
  | (HomeStandingsBase & {
      viewType: "bracket";
      finalist: {
        teamId: string;
        teamName: string;
        fromGroupName: string;
      } | null;
      opponent: {
        teamId: string;
        teamName: string;
        fromGroupName: string;
      } | null;
    });

export type HomePhasesResponse = {
  phases: HomePhase[];
};
