import { backendFetch } from "@/lib/api/client";
import type { HomeHighlightsResponse } from "../types/highlights";

const BASE = "/views/home/highlights?season=2026&tournament=Apertura";

export async function getHomeHighlights(): Promise<HomeHighlightsResponse> {
  return backendFetch<HomeHighlightsResponse>(BASE);
}
