import type { MatchStatus } from "../types/shared";

export function formatMatchStatus(status: MatchStatus) {
  const labels: Record<MatchStatus, string> = {
    scheduled: "Programado",
    live: "En vivo",
    finished: "Final",
    postponed: "Postergado",
    cancelled: "Cancelado",
  };

  return labels[status];
}
