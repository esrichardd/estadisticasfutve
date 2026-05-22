type HomeShellProps = {
  children: React.ReactNode;
  labels: {
    brand: {
      prefix: string;
      accent: string;
      short: string;
    };
    nav: string[];
    footerBrand: string;
    footerNote: string;
  };
};

export function HomeShell({ children, labels }: HomeShellProps) {
  return (
    <div className="min-h-screen bg-background">
      <nav className="sticky top-0 z-50 border-b border-border bg-card">
        <div className="mx-auto flex h-12 max-w-[1400px] items-center justify-between px-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-7 w-7 items-center justify-center rounded-sm bg-primary">
              <span className="text-[10px] font-black tracking-tight text-primary-foreground">
                {labels.brand.short}
              </span>
            </div>
            <span className="text-sm font-bold tracking-wide text-foreground">
              {labels.brand.prefix}{" "}
              <span className="text-secondary">{labels.brand.accent}</span>
            </span>
          </div>

          <ul className="hidden items-center gap-1 md:flex">
            {labels.nav.map((link, index) => (
              <li key={link}>
                <a
                  className={`rounded-sm px-3 py-1.5 text-sm font-medium transition-colors ${
                    index === 0
                      ? "border-b-2 border-secondary pb-[5px] text-secondary"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                  href="#"
                >
                  {link}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      <main className="mx-auto max-w-[1400px] space-y-4 px-4 py-4">
        {children}
      </main>

      <footer className="mx-auto mt-4 max-w-[1400px] border-t border-border px-4 py-6">
        <div className="flex flex-col items-center justify-between gap-2 sm:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-5 w-5 items-center justify-center rounded-sm bg-primary">
              <span className="text-[8px] font-black text-primary-foreground">
                {labels.brand.short}
              </span>
            </div>
            <span className="text-xs font-semibold text-muted-foreground">
              {labels.footerBrand}
            </span>
          </div>
          <p className="text-[11px] text-muted-foreground">
            {labels.footerNote}
          </p>
        </div>
      </footer>
    </div>
  );
}
