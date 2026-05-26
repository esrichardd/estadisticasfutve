import { backendFetch } from "@/lib/api/client";
import type { HomeSummaryResponse } from "../types/summary";

const BASE = "/views/home/summary?season=2026&tournament=Apertura";

export async function getHomeSummary(): Promise<HomeSummaryResponse> {
  const data = await backendFetch<HomeSummaryResponse>(BASE);

  // El componente muestra metrics.nextMatch como string display-ready.
  // El backend devuelve ISO UTC; lo convertimos aquí para no tocar el componente.
  const nextMatchRaw = data.metrics.nextMatch;
  const nextMatchFormatted =
    nextMatchRaw
      ? new Intl.DateTimeFormat("es", {
          weekday: "short",
          day: "2-digit",
          month: "short",
          hour: "2-digit",
          minute: "2-digit",
        }).format(new Date(nextMatchRaw))
      : "—";

  return {
    ...data,
    metrics: {
      ...data.metrics,
      nextMatch: nextMatchFormatted,
    },
  };
}
