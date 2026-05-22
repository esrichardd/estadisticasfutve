import { mockStandings } from "./mock-home-data";

export function getHomeStandings() {
  return Promise.resolve(mockStandings);
}
