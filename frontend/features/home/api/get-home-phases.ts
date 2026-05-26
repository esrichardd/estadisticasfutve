import type { HomePhasesResponse } from "../types/standings";
import { mockPhases } from "./mock-home-data";

export function getHomePhasesResponse(): Promise<HomePhasesResponse> {
  return Promise.resolve({
    phases: mockPhases,
  });
}
