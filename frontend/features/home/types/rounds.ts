import type { MatchStatus, TeamSummary } from "./shared";

export type HomeMatch = {
  id: string;
  status: MatchStatus;
  scheduledDatetime: string;
  venue: string | null;
  homeTeam: TeamSummary;
  awayTeam: TeamSummary;
  homeScore: number | null;
  awayScore: number | null;
  liveMinute?: number;
};

export type HomeRound = {
  id: string;
  number: number;
  name: string;
  dateStart: string;
  dateEnd: string;
  matches: HomeMatch[];
};

export type HomeRoundsResponse = {
  latest: HomeRound | null;
  next: HomeRound | null;
};
