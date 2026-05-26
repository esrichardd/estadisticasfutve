import { backendFetch } from "@/lib/api/client";
import type { HomeRoundsResponse } from "../types/rounds";

const BASE = "/views/home/rounds?season=2026&tournament=Apertura";

export async function getHomeRounds(): Promise<HomeRoundsResponse> {
  return backendFetch<HomeRoundsResponse>(BASE);
}
