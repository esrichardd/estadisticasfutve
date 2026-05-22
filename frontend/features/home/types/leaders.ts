import type { PlayerSummary, TeamSummary } from "./shared";

export type PlayerLeader = {
  player: PlayerSummary;
  team: TeamSummary;
  value: number;
};

export type HomeLeadersResponse = {
  scorers: PlayerLeader[];
  assisters: PlayerLeader[];
};
