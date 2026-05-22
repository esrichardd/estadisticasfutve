import { Skeleton } from "@/components/ui/skeleton";
import { getHomeRounds } from "../../api/get-home-rounds";
import { RoundsTabs } from "./rounds-tabs";

type HomeRoundsLabels = {
  latestRound: string;
  roundShort: string;
  round: string;
  empty: string;
  liveMatchSingular: string;
  liveMatchPlural: string;
  status: {
    finished: string;
    scheduledShort: string;
  };
};

type HomeRoundsProps =
  | { skeleton: true }
  | { skeleton?: false; labels: HomeRoundsLabels; formatLocale: string };

export async function HomeRounds(props: HomeRoundsProps) {
  if (props.skeleton) {
    return (
      <section className="overflow-hidden rounded-sm border border-border bg-card">
        <div className="grid grid-cols-2 border-b border-border">
          <Skeleton className="m-2 h-6 w-auto" />
          <Skeleton className="m-2 h-6 w-auto" />
        </div>
        {Array.from({ length: 6 }).map((_, index) => (
          <Skeleton className="m-3 h-9 w-auto" key={index} />
        ))}
      </section>
    );
  }

  const rounds = await getHomeRounds();

  return (
    <RoundsTabs
      formatLocale={props.formatLocale}
      labels={props.labels}
      latest={rounds.latest}
      next={rounds.next}
    />
  );
}
