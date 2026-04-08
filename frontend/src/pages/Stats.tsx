import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faDatabase,
  faTag,
  faBullseye,
  faLayerGroup,
  faChartPie,
  faChartBar,
  faShieldHalved,
  faBolt,
} from "@fortawesome/free-solid-svg-icons";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { MOCK_STATS, CATEGORY_DATA, TOP_INTENTS } from "@/lib/api";

const metricCards = [
  {
    label: "Total Records",
    value: "25,545",
    icon: faDatabase,
    color: "text-blue-500",
    bg: "bg-blue-50 dark:bg-blue-900/20",
    desc: "Banking interaction records",
  },
  {
    label: "Categories",
    value: "9",
    icon: faLayerGroup,
    color: "text-purple-500",
    bg: "bg-purple-50 dark:bg-purple-900/20",
    desc: "Banking service categories",
  },
  {
    label: "Intents",
    value: "26",
    icon: faTag,
    color: "text-emerald-500",
    bg: "bg-emerald-50 dark:bg-emerald-900/20",
    desc: "Distinct customer intents",
  },
  {
    label: "Overall Accuracy",
    value: "91%",
    icon: faBullseye,
    color: "text-amber-500",
    bg: "bg-amber-50 dark:bg-amber-900/20",
    desc: "System-wide accuracy",
  },
];

const accuracyComponents = [
  { label: "Intent Classification", value: MOCK_STATS.intent_accuracy, color: "#3b82f6" },
  { label: "Chunk Retrieval", value: MOCK_STATS.retrieval_accuracy, color: "#8b5cf6" },
  { label: "Response Generation", value: MOCK_STATS.generation_accuracy, color: "#10b981" },
];

const dataQuality = [
  { metric: "Whitespace Issues", before: 15432, after: 0 },
  { metric: "Inconsistent Format", before: 12890, after: 0 },
  { metric: "Special Chars", before: 8765, after: 2341 },
  { metric: "Typos Found", before: 3083, after: 6 },
];

const CustomTooltip = ({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
}) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border border-border rounded-xl px-3 py-2 shadow-md text-sm">
        {label && <p className="font-medium text-foreground mb-1">{label}</p>}
        {payload.map((p) => (
          <p key={p.name} style={{ color: p.color }}>
            {p.name}: {p.value.toLocaleString()}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function Stats() {
  return (
    <div className="h-full overflow-y-auto px-6 py-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="fade-in-up">
          <h1 className="text-2xl font-semibold text-foreground">System Statistics</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Dataset analysis and model performance metrics for the Banking Assistant System
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 fade-in-up">
          {metricCards.map(({ label, value, icon, color, bg, desc }) => (
            <div
              key={label}
              data-testid={`card-metric-${label.toLowerCase().replace(/\s/g, "-")}`}
              className="bg-card border border-border rounded-2xl p-5 hover:shadow-md transition-shadow"
            >
              <div className={`w-10 h-10 rounded-xl ${bg} flex items-center justify-center mb-3`}>
                <FontAwesomeIcon icon={icon} className={`${color} text-lg`} />
              </div>
              <p className="text-2xl font-bold text-foreground">{value}</p>
              <p className="text-sm font-medium text-foreground mt-0.5">{label}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{desc}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-card border border-border rounded-2xl p-5 fade-in-up">
            <div className="flex items-center gap-2 mb-4">
              <FontAwesomeIcon icon={faChartPie} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Category Distribution</h2>
            </div>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={CATEGORY_DATA}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="45%"
                  outerRadius={90}
                  innerRadius={45}
                  paddingAngle={2}
                  isAnimationActive={true}
                >
                  {CATEGORY_DATA.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const d = payload[0].payload as (typeof CATEGORY_DATA)[0];
                      return (
                        <div className="bg-card border border-border rounded-xl px-3 py-2 shadow-md text-sm">
                          <p className="font-medium text-foreground">{d.name}</p>
                          <p className="text-muted-foreground">{d.count.toLocaleString()} records</p>
                          <p className="text-muted-foreground">{d.percentage}%</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Legend
                  formatter={(value) => <span className="text-xs text-muted-foreground">{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-card border border-border rounded-2xl p-5 fade-in-up">
            <div className="flex items-center gap-2 mb-4">
              <FontAwesomeIcon icon={faChartBar} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Top 10 Intents</h2>
            </div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={TOP_INTENTS} layout="vertical" margin={{ left: 0, right: 10 }}>
                <XAxis type="number" tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={140}
                  tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
                  tickFormatter={(v: string) => v.replace(/_/g, " ")}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Records" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-card border border-border rounded-2xl p-5 fade-in-up">
            <div className="flex items-center gap-2 mb-5">
              <FontAwesomeIcon icon={faBullseye} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Model Accuracy</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <FontAwesomeIcon icon={faBolt} className="text-amber-500 text-sm" />
                  <span className="text-sm font-medium text-foreground">Overall Accuracy</span>
                </div>
                <span className="text-2xl font-bold text-foreground">91%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2 mb-5">
                <div className="bg-amber-500 h-2 rounded-full" style={{ width: "91%" }} />
              </div>
              {accuracyComponents.map(({ label, value, color }) => (
                <div key={label} data-testid={`accuracy-${label.toLowerCase().replace(/\s/g, "-")}`}>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="text-sm text-muted-foreground">{label}</span>
                    <span className="text-sm font-semibold text-foreground">{value}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-1.5">
                    <div
                      className="h-1.5 rounded-full transition-all duration-700"
                      style={{ width: `${value}%`, backgroundColor: color }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-card border border-border rounded-2xl p-5 fade-in-up">
            <div className="flex items-center gap-2 mb-5">
              <FontAwesomeIcon icon={faShieldHalved} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Data Quality Improvements</h2>
            </div>
            <div className="space-y-3">
              {dataQuality.map(({ metric, before, after }) => {
                const improvement = before > 0 ? Math.round(((before - after) / before) * 100) : 100;
                return (
                  <div
                    key={metric}
                    data-testid={`quality-metric-${metric.toLowerCase().replace(/\s/g, "-")}`}
                    className="flex items-center justify-between py-2 border-b border-border last:border-0"
                  >
                    <span className="text-sm text-foreground flex-1">{metric}</span>
                    <div className="flex items-center gap-3 text-sm">
                      <span className="text-muted-foreground">{before.toLocaleString()}</span>
                      <span className="text-muted-foreground">→</span>
                      <span className="text-foreground font-medium">{after.toLocaleString()}</span>
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                          improvement === 100
                            ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
                            : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                        }`}
                      >
                        {improvement}% fixed
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-2xl p-5 fade-in-up">
          <div className="flex items-center gap-2 mb-5">
            <FontAwesomeIcon icon={faDatabase} className="text-primary text-sm" />
            <h2 className="font-semibold text-foreground">Dataset Overview</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2.5 pr-4 font-semibold text-foreground">Category</th>
                  <th className="text-right py-2.5 px-4 font-semibold text-foreground">Records</th>
                  <th className="text-right py-2.5 px-4 font-semibold text-foreground">Percentage</th>
                  <th className="text-left py-2.5 pl-4 font-semibold text-foreground">Distribution</th>
                </tr>
              </thead>
              <tbody>
                {CATEGORY_DATA.map(({ name, count, percentage, color }) => (
                  <tr
                    key={name}
                    data-testid={`row-category-${name.toLowerCase()}`}
                    className="border-b border-border/50 last:border-0 hover:bg-muted/30 transition-colors"
                  >
                    <td className="py-2.5 pr-4">
                      <div className="flex items-center gap-2">
                        <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
                        <span className="font-medium text-foreground">{name}</span>
                      </div>
                    </td>
                    <td className="text-right py-2.5 px-4 text-muted-foreground">{count.toLocaleString()}</td>
                    <td className="text-right py-2.5 px-4 text-muted-foreground">{percentage}%</td>
                    <td className="py-2.5 pl-4 min-w-[120px]">
                      <div className="w-full bg-muted rounded-full h-1.5">
                        <div
                          className="h-1.5 rounded-full transition-all duration-700"
                          style={{ width: `${percentage}%`, backgroundColor: color }}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
