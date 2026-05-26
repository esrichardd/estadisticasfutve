import type { HomeHighlightsResponse } from "../types/highlights";
import type { HomeLeadersResponse } from "../types/leaders";
import type { HomeRoundsResponse } from "../types/rounds";
import type { TeamSummary } from "../types/shared";
import type {
  HomePhase,
  HomeStandingRow,
  HomeStandingsResponse,
} from "../types/standings";
import type { HomeSummaryResponse } from "../types/summary";

const teams: TeamSummary[] = [
  ["tachira", "Deportivo Táchira", "Táchira", "TAC", "#8B0000"],
  ["caracas", "Caracas Futbol Club", "Caracas", "CAR", "#CC0000"],
  ["laguaira", "Deportivo La Guaira", "La Guaira", "LGU", "#1A5276"],
  ["monagas", "Monagas Sport Club", "Monagas", "MON", "#7D3C98"],
  ["metro", "Metropolitanos FC", "Metropolitanos", "MET", "#1A6B3C"],
  ["portuguesa", "Portuguesa FC", "Portuguesa", "POR", "#C0392B"],
  ["carabobo", "Carabobo FC", "Carabobo", "CAB", "#6E2F1A"],
  ["zamora", "Zamora FC", "Zamora", "ZAM", "#F39C12"],
  ["rayo", "Deportivo Rayo Zuliano", "Rayo Zuliano", "RAY", "#2874A6"],
  ["estudiantes", "Estudiantes de Mérida", "Estudiantes", "EST", "#117A65"],
  ["angostura", "Angostura FC", "Angostura", "ANG", "#1F618D"],
  ["ucv", "UCV FC", "UCV FC", "UCV", "#B7950B"],
  ["academia", "Academia Puerto Cabello", "Puerto Cabello", "APC", "#D4AC0D"],
  ["yaracuyanos", "Yaracuyanos FC", "Yaracuyanos", "YAR", "#196F3D"],
].map(([id, name, shortName, abbreviation, color]) => ({
  id,
  name,
  shortName,
  abbreviation,
  color,
  logoUrl: null,
}));

const team = (id: string) => teams.find((item) => item.id === id) ?? teams[0];

const standingRows = (
  rows: [
    number,
    string,
    number,
    number,
    number,
    number,
    number,
    number,
    number,
    number,
    HomeStandingRow["form"],
  ][],
): HomeStandingRow[] =>
  rows.map(
    ([
      position,
      teamId,
      played,
      won,
      drawn,
      lost,
      goalsFor,
      goalsAgainst,
      goalDifference,
      points,
      form,
    ]) => ({
      position,
      team: team(teamId),
      played,
      won,
      drawn,
      lost,
      goalsFor,
      goalsAgainst,
      goalDifference,
      points,
      form,
    }),
  );

export const mockSummary: HomeSummaryResponse = {
  league: {
    id: "liga-futve",
    name: "Liga FUTVE",
    logoUrl: null,
  },
  season: {
    id: "season-2026",
    displayName: "2026",
  },
  tournament: {
    id: "apertura-2026",
    name: "Apertura",
  },
  phase: {
    id: "ronda-regular",
    name: "Ronda Regular",
    type: "round_robin",
  },
  currentRound: {
    id: "jornada-8",
    number: 8,
    name: "Jornada 8",
  },
  metrics: {
    leader: {
      teamName: "Táchira",
      points: 17,
    },
    totalGoals: 99,
    playedMatches: 48,
    nextMatch: "Táchira vs La Guaira",
  },
  lastUpdated: "2026-05-22T18:42:00-05:00",
};

export const mockPhases: HomePhase[] = [
  {
    id: "regular",
    name: "Ronda Regular",
    type: "round_robin",
    isCurrent: true,
  },
  {
    id: "cuadrangulares",
    name: "Cuadrangulares",
    type: "group_stage",
    isCurrent: false,
  },
  {
    id: "final",
    name: "Final",
    type: "knockout",
    isCurrent: false,
  },
];

export const mockStandingsByPhase: Record<string, HomeStandingsResponse> = {
  regular: {
    phaseId: "regular",
    groupId: null,
    viewType: "single_table",
    highlights: [
      {
        key: "qualifiesKnockout",
        tone: "promotion",
        from: 1,
        to: 8,
      },
      {
        key: "relegation",
        tone: "danger",
        from: 13,
        to: 14,
      },
    ],
    rows: standingRows([
      [1, "tachira", 8, 5, 2, 1, 17, 8, 9, 17, ["W", "W", "D", "W", "W"]],
      [2, "caracas", 8, 5, 1, 2, 14, 9, 5, 16, ["W", "D", "W", "W", "L"]],
      [3, "laguaira", 8, 4, 2, 2, 12, 8, 4, 14, ["W", "L", "W", "D", "W"]],
      [4, "metro", 8, 4, 1, 3, 11, 11, 0, 13, ["D", "W", "W", "L", "W"]],
      [5, "monagas", 8, 3, 3, 2, 10, 9, 1, 12, ["W", "D", "L", "W", "D"]],
      [6, "portuguesa", 8, 3, 2, 3, 9, 10, -1, 11, ["L", "W", "D", "W", "L"]],
      [7, "zamora", 8, 3, 1, 4, 10, 13, -3, 10, ["W", "L", "L", "W", "D"]],
      [8, "carabobo", 8, 2, 3, 3, 8, 10, -2, 9, ["D", "D", "L", "W", "D"]],
      [9, "rayo", 8, 2, 2, 4, 7, 12, -5, 8, ["L", "W", "D", "L", "W"]],
      [10, "estudiantes", 8, 2, 1, 5, 8, 14, -6, 7, ["L", "L", "W", "D", "L"]],
      [11, "academia", 8, 1, 4, 3, 7, 11, -4, 7, ["D", "D", "L", "D", "W"]],
      [12, "yaracuyanos", 8, 1, 3, 4, 6, 13, -7, 6, ["L", "D", "D", "W", "L"]],
      [13, "angostura", 8, 1, 2, 5, 5, 13, -8, 5, ["D", "L", "L", "W", "L"]],
      [14, "ucv", 8, 1, 0, 7, 4, 18, -14, 3, ["L", "L", "L", "W", "L"]],
    ]),
  },
  cuadrangulares: {
    phaseId: "cuadrangulares",
    groupId: null,
    viewType: "grouped_tables",
    highlights: [
      {
        key: "qualifiesFinal",
        tone: "promotion",
        from: 1,
        to: 1,
      },
    ],
    groups: [
      {
        id: "grupo-a",
        name: "Cuadrangular A",
        rows: standingRows([
          [1, "tachira", 2, 2, 0, 0, 4, 1, 3, 6, ["W", "W", "D", "W", "W"]],
          [2, "laguaira", 2, 1, 0, 1, 3, 3, 0, 3, ["W", "L", "W", "D", "W"]],
          [3, "monagas", 2, 0, 1, 1, 2, 3, -1, 1, ["W", "D", "L", "W", "D"]],
          [4, "carabobo", 2, 0, 1, 1, 1, 3, -2, 1, ["D", "D", "L", "W", "D"]],
        ]),
      },
      {
        id: "grupo-b",
        name: "Cuadrangular B",
        rows: standingRows([
          [1, "caracas", 2, 1, 1, 0, 3, 1, 2, 4, ["W", "D", "W", "W", "L"]],
          [2, "metro", 2, 1, 1, 0, 2, 1, 1, 4, ["D", "W", "W", "L", "W"]],
          [3, "portuguesa", 2, 1, 0, 1, 2, 2, 0, 3, ["L", "W", "D", "W", "L"]],
          [4, "zamora", 2, 0, 0, 2, 1, 4, -3, 0, ["W", "L", "L", "W", "D"]],
        ]),
      },
    ],
  },
  final: {
    phaseId: "final",
    groupId: null,
    viewType: "bracket",
    highlights: [],
    finalist: {
      teamId: "tachira",
      teamName: "Deportivo Táchira",
      fromGroupName: "Cuadrangular A",
    },
    opponent: null,
  },
};

export const mockStandings: HomeStandingsResponse =
  mockStandingsByPhase.regular;

export const mockRounds: HomeRoundsResponse = {
  latest: {
    id: "jornada-7",
    number: 7,
    name: "Jornada 7",
    dateStart: "2026-05-16",
    dateEnd: "2026-05-18",
    matches: [
      {
        id: "match-1",
        status: "finished",
        scheduledDatetime: "2026-05-18T19:00:00-05:00",
        venue: "Pueblo Nuevo",
        homeTeam: team("tachira"),
        awayTeam: team("angostura"),
        homeScore: 3,
        awayScore: 0,
      },
      {
        id: "match-2",
        status: "finished",
        scheduledDatetime: "2026-05-18T17:00:00-05:00",
        venue: "Estadio Olimpico UCV",
        homeTeam: team("caracas"),
        awayTeam: team("ucv"),
        homeScore: 2,
        awayScore: 1,
      },
      {
        id: "match-3",
        status: "finished",
        scheduledDatetime: "2026-05-17T19:00:00-05:00",
        venue: "Olimpico UCV",
        homeTeam: team("metro"),
        awayTeam: team("rayo"),
        homeScore: 1,
        awayScore: 0,
      },
      {
        id: "match-4",
        status: "finished",
        scheduledDatetime: "2026-05-17T17:00:00-05:00",
        venue: "Jose Antonio Paez",
        homeTeam: team("portuguesa"),
        awayTeam: team("zamora"),
        homeScore: 1,
        awayScore: 2,
      },
      {
        id: "match-5",
        status: "finished",
        scheduledDatetime: "2026-05-16T19:00:00-05:00",
        venue: "Monumental de Maturin",
        homeTeam: team("monagas"),
        awayTeam: team("carabobo"),
        homeScore: 1,
        awayScore: 1,
      },
      {
        id: "match-6",
        status: "finished",
        scheduledDatetime: "2026-05-16T17:00:00-05:00",
        venue: "Estadio Olimpico UCV",
        homeTeam: team("laguaira"),
        awayTeam: team("estudiantes"),
        homeScore: 2,
        awayScore: 0,
      },
    ],
  },
  next: {
    id: "jornada-8",
    number: 8,
    name: "Jornada 8",
    dateStart: "2026-05-24",
    dateEnd: "2026-05-25",
    matches: [
      {
        id: "match-7",
        status: "scheduled",
        scheduledDatetime: "2026-05-24T19:00:00-05:00",
        venue: "Pueblo Nuevo",
        homeTeam: team("tachira"),
        awayTeam: team("laguaira"),
        homeScore: null,
        awayScore: null,
      },
      {
        id: "match-8",
        status: "scheduled",
        scheduledDatetime: "2026-05-24T17:00:00-05:00",
        venue: "Estadio Olimpico UCV",
        homeTeam: team("caracas"),
        awayTeam: team("metro"),
        homeScore: null,
        awayScore: null,
      },
      {
        id: "match-9",
        status: "live",
        scheduledDatetime: "2026-05-25T15:30:00-05:00",
        venue: "Agustin Tovar",
        homeTeam: team("zamora"),
        awayTeam: team("monagas"),
        homeScore: 1,
        awayScore: 1,
        liveMinute: 67,
      },
      {
        id: "match-10",
        status: "live",
        scheduledDatetime: "2026-05-25T17:00:00-05:00",
        venue: "Misael Delgado",
        homeTeam: team("carabobo"),
        awayTeam: team("portuguesa"),
        homeScore: 0,
        awayScore: 0,
        liveMinute: 32,
      },
      {
        id: "match-11",
        status: "scheduled",
        scheduledDatetime: "2026-05-25T19:00:00-05:00",
        venue: "Pachencho Romero",
        homeTeam: team("rayo"),
        awayTeam: team("angostura"),
        homeScore: null,
        awayScore: null,
      },
      {
        id: "match-12",
        status: "scheduled",
        scheduledDatetime: "2026-05-25T15:00:00-05:00",
        venue: "Metropolitano de Merida",
        homeTeam: team("estudiantes"),
        awayTeam: team("ucv"),
        homeScore: null,
        awayScore: null,
      },
    ],
  },
};

export const mockLeaders: HomeLeadersResponse = {
  scorers: [
    ["pena", "Ronaldo Peña", "Delantero", "tachira", 7],
    ["morales", "Miguel Morales", "Delantero", "caracas", 6],
    ["suarez", "Javier Suárez", "Delantero", "laguaira", 5],
    ["rivas", "Carlos Rivas", "Extremo", "metro", 4],
    ["gutierrez", "Freddy Gutiérrez", "Delantero", "monagas", 4],
  ].map(([id, name, position, teamId, value]) => ({
    player: { id: String(id), name: String(name), position: String(position) },
    team: team(String(teamId)),
    value: Number(value),
  })),
  assisters: [
    ["soteldo", "Yeferson Soteldo", "Extremo", "caracas", 6],
    ["henriquez", "Amílcar Henríquez", "Volante", "tachira", 5],
    ["febles", "Omar Febles", "Volante", "laguaira", 4],
    ["machis", "Darwin Machis", "Extremo", "metro", 3],
    ["murillo", "Jhon Murillo", "Extremo", "portuguesa", 3],
  ].map(([id, name, position, teamId, value]) => ({
    player: { id: String(id), name: String(name), position: String(position) },
    team: team(String(teamId)),
    value: Number(value),
  })),
};

export const mockHighlights: HomeHighlightsResponse = {
  bestAttack: {
    team: team("tachira"),
    goalsFor: 17,
  },
  bestDefense: {
    team: team("tachira"),
    goalsAgainst: 8,
  },
  bestGoalDifference: {
    team: team("tachira"),
    goalDifference: 9,
  },
};
