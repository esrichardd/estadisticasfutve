import { backendFetch } from "@/lib/api/client";
import type { HomePhasesResponse } from "../types/standings";

const BASE = "/views/home/phases?season=2026&tournament=Apertura";

export async function getHomePhasesResponse(): Promise<HomePhasesResponse> {
  return backendFetch<HomePhasesResponse>(BASE);
}
