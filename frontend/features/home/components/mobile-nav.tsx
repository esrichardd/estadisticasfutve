"use client";

import { Menu, X } from "lucide-react";
import { useState } from "react";

type MobileNavProps = {
  links: string[];
  labels: {
    open: string;
    close: string;
  };
};

export function MobileNav({ labels, links }: MobileNavProps) {
  const [isOpen, setIsOpen] = useState(false);
  const label = isOpen ? labels.close : labels.open;

  return (
    <div className="md:hidden">
      <button
        aria-expanded={isOpen}
        aria-label={label}
        className="flex h-8 w-8 items-center justify-center rounded-sm border border-border bg-accent text-foreground transition-colors hover:border-secondary hover:bg-secondary/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-secondary"
        onClick={() => setIsOpen((current) => !current)}
        title={label}
        type="button"
      >
        {isOpen ? <X size={16} /> : <Menu size={16} />}
      </button>

      {isOpen ? (
        <div className="absolute left-0 right-0 top-12 border-b border-border bg-card px-4 py-2 shadow-lg">
          <ul className="mx-auto grid max-w-[1400px] gap-1">
            {links.map((link, index) => (
              <li key={link}>
                <a
                  className={`block rounded-sm px-3 py-2 text-sm font-medium transition-colors ${
                    index === 0
                      ? "bg-secondary/10 text-secondary"
                      : "text-muted-foreground hover:bg-accent hover:text-foreground"
                  }`}
                  href="#"
                  onClick={() => setIsOpen(false)}
                >
                  {link}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
