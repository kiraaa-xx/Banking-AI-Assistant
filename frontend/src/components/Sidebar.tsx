import { Link, useLocation } from "wouter";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faComments,
  faChartPie,
  faCircleInfo,
  faSun,
  faMoon,
  faBars,
  faXmark,
  faBuilding,
  faShieldHalved,
} from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";

interface SidebarProps {
  isDark: boolean;
  onToggleDark: () => void;
}

const navItems = [
  { href: "/", label: "Assistant", icon: faComments },
  { href: "/stats", label: "Statistics", icon: faChartPie },
  { href: "/about", label: "About System", icon: faCircleInfo },
];

export function Sidebar({ isDark, onToggleDark }: SidebarProps) {
  const [location] = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const NavContent = () => (
    <>
      <div className="flex items-center gap-3 px-5 pt-7 pb-6 border-b border-sidebar-border">
        <div className="w-9 h-9 rounded-xl bg-blue-500/20 flex items-center justify-center flex-shrink-0">
          <FontAwesomeIcon icon={faBuilding} className="text-blue-400 text-sm" />
        </div>
        <div>
          <p className="text-sidebar-foreground font-semibold text-[15px] leading-tight">Banking AI</p>
          <p className="text-sidebar-foreground/50 text-[11px] mt-0.5">LLM + RAG System</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ href, label, icon }) => {
          const active = location === href || (href !== "/" && location.startsWith(href));
          return (
            <Link
              key={href}
              href={href}
              onClick={() => setMobileOpen(false)}
              data-testid={`nav-link-${label.toLowerCase().replace(/\s/g, "-")}`}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 cursor-pointer ${
                active
                  ? "bg-sidebar-primary text-sidebar-primary-foreground"
                  : "text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-foreground"
              }`}
            >
              <FontAwesomeIcon icon={icon} className="w-4 h-4 flex-shrink-0" />
              <span>{label}</span>
              {active && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-current opacity-70" />}
            </Link>
          );
        })}
      </nav>

      <div className="px-3 pb-6 space-y-2">
        <div className="mx-2 mb-3 px-3 py-2.5 rounded-lg bg-sidebar-accent/50 text-sidebar-foreground/60 text-xs">
          <div className="flex items-center gap-2 mb-1.5">
            <FontAwesomeIcon icon={faShieldHalved} className="text-green-400 text-xs" />
            <span className="font-medium text-sidebar-foreground/80">System Accuracy</span>
          </div>
          <div className="space-y-1">
            {[
              { label: "Intent Classification", value: "92%" },
              { label: "Chunk Retrieval", value: "89%" },
              { label: "Response Generation", value: "91%" },
            ].map(({ label, value }) => (
              <div key={label} className="flex justify-between items-center">
                <span>{label}</span>
                <span className="text-green-400 font-medium">{value}</span>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={onToggleDark}
          data-testid="button-toggle-theme"
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-foreground transition-all duration-150 cursor-pointer"
        >
          <FontAwesomeIcon icon={isDark ? faSun : faMoon} className="w-4 h-4" />
          <span>{isDark ? "Light Mode" : "Dark Mode"}</span>
        </button>
      </div>
    </>
  );

  return (
    <>
      <button
        className="lg:hidden fixed top-4 left-4 z-50 w-10 h-10 flex items-center justify-center rounded-xl bg-sidebar text-sidebar-foreground shadow-lg"
        onClick={() => setMobileOpen(!mobileOpen)}
        data-testid="button-mobile-menu"
      >
        <FontAwesomeIcon icon={mobileOpen ? faXmark : faBars} />
      </button>

      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 z-40 bg-black/50"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-64 bg-sidebar flex flex-col transition-transform duration-300 ${
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <NavContent />
      </aside>
    </>
  );
}
