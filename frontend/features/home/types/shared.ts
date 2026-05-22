export type TeamSummary = {
  id: string;
  name: string;
  shortName: string;
  abbreviation: string;
  color: string;
  logoUrl: string | null;
};

export type PlayerSummary = {
  id: string;
  name: string;
  position: string | null;
};

export type MatchStatus =
  | "scheduled"
  | "live"
  | "finished"
  | "postponed"
  | "cancelled";

export type FormResult = "W" | "D" | "L";
