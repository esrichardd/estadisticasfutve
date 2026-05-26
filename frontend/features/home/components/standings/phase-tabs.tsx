"use client";

import { startTransition, useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { HomePhase, HomePhaseType } from "../../types/standings";

type PhaseTabsProps = {
  phases: HomePhase[];
  activeParam: string | null;
  labels: {
    current: string;
    names: Record<HomePhaseType, string>;
  };
};

export function PhaseTabs({ activeParam, labels, phases }: PhaseTabsProps) {
  const pathname = usePathname();
  const router = useRouter();
  const searchParams = useSearchParams();
  const currentPhase = phases.find((phase) => phase.isCurrent);
  const selectedPhaseId = activeParam ?? currentPhase?.id ?? phases[0]?.id;

  const paramsSnapshot = useMemo(() => searchParams.toString(), [searchParams]);

  const selectPhase = (phase: HomePhase) => {
    const nextParams = new URLSearchParams(paramsSnapshot);

    if (phase.isCurrent) {
      nextParams.delete("phase");
    } else {
      nextParams.set("phase", phase.id);
    }

    const query = nextParams.toString();
    const href = query ? `${pathname}?${query}` : pathname;

    startTransition(() => {
      router.push(href, { scroll: false });
    });
  };

  if (phases.length <= 1) {
    return null;
  }

  return (
    <div className="border-b border-border px-2 py-2">
      <div className="flex gap-1 overflow-x-auto">
        {phases.map((phase) => {
          const isSelected = phase.id === selectedPhaseId;
          const label = labels.names[phase.type] ?? phase.name;

          return (
            <button
              aria-pressed={isSelected}
              className={`flex min-h-8 shrink-0 items-center gap-1.5 rounded-sm px-2.5 text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary ${
                isSelected
                  ? "bg-secondary text-secondary-foreground"
                  : "bg-accent text-muted-foreground hover:text-foreground"
              }`}
              key={phase.id}
              onClick={() => selectPhase(phase)}
              type="button"
            >
              {phase.isCurrent ? (
                <span
                  aria-label={labels.current}
                  className="h-1.5 w-1.5 rounded-full bg-win"
                  title={labels.current}
                />
              ) : null}
              <span>{label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
