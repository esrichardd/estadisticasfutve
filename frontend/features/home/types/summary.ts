export type HomeSummaryResponse = {
  league: {
    id: string;
    name: string;
    logoUrl: string | null;
  };
  season: {
    id: string;
    displayName: string;
  };
  tournament: {
    id: string;
    name: string;
  };
  phase: {
    id: string;
    name: string;
    type: "round_robin" | "group_stage" | "knockout" | "two_legged";
  };
  currentRound: {
    id: string;
    number: number;
    name: string;
  } | null;
  metrics: {
    leader: {
      teamName: string;
      points: number;
    };
    totalGoals: number;
    playedMatches: number;
    nextMatch: string;
  };
  lastUpdated: string | null;
};
