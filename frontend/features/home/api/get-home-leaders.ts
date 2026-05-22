import { mockLeaders } from "./mock-home-data";

export function getHomeLeaders() {
  return Promise.resolve(mockLeaders);
}
