import { Skeleton } from "@/components/ui/skeleton";
import { getHomeRounds } from "../../api/get-home-rounds";
import { RoundsTabs } from "./rounds-tabs";

type HomeRoundsProps = { skeleton: true } | { skeleton?: false };

export async function HomeRounds({ skeleton = false }: HomeRoundsProps) {
  if (skeleton) {
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

  return <RoundsTabs latest={rounds.latest} next={rounds.next} />;
}
