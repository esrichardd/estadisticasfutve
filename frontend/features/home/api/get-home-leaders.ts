import { backendFetch } from "@/lib/api/client";
import type { HomeLeadersResponse } from "../types/leaders";

const BASE = "/views/home/leaders?season=2026&tournament=Apertura";

export async function getHomeLeaders(): Promise<HomeLeadersResponse> {
  return backendFetch<HomeLeadersResponse>(BASE);
}
