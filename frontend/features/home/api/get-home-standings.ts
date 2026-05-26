import { mockPhases, mockStandingsByPhase } from "./mock-home-data";

export function getHomeStandings(phaseId?: string) {
  const currentPhase = mockPhases.find((phase) => phase.isCurrent);
  const fallbackPhaseId = currentPhase?.id ?? mockPhases[0]?.id;
  const requestedPhaseId = phaseId?.trim();
  const standings =
    (requestedPhaseId ? mockStandingsByPhase[requestedPhaseId] : undefined) ??
    (fallbackPhaseId ? mockStandingsByPhase[fallbackPhaseId] : undefined);

  if (!standings) {
    throw new Error("No standings mock is configured.");
  }

  return Promise.resolve(standings);
}
