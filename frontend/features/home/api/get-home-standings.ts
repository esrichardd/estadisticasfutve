import { backendFetch } from "@/lib/api/client";
import type { HomeStandingsResponse } from "../types/standings";

const BASE = "/views/home/standings?season=2026&tournament=Apertura";

export async function getHomeStandings(
  phaseId?: string
): Promise<HomeStandingsResponse> {
  const path = phaseId ? `${BASE}&phase_id=${phaseId}` : BASE;
  return backendFetch<HomeStandingsResponse>(path);
}
