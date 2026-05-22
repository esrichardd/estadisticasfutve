import type { MatchStatus } from "../types/shared";

export function formatMatchStatus(
  status: MatchStatus,
  labels: Record<MatchStatus, string>,
) {
  return labels[status];
}
