interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({ content, className = "" }: MarkdownRendererProps) {
  const lines = content.split("\n");
  const rendered: JSX.Element[] = [];
  let listItems: string[] = [];
  let tableLines: string[] = [];
  let inTable = false;

  const flushList = (key: string) => {
    if (listItems.length > 0) {
      rendered.push(
        <ul key={`ul-${key}`} className="my-2 space-y-1">
          {listItems.map((item, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-primary flex-shrink-0" />
              <span dangerouslySetInnerHTML={{ __html: formatInline(item) }} />
            </li>
          ))}
        </ul>
      );
      listItems = [];
    }
  };

  const flushTable = (key: string) => {
    if (tableLines.length >= 2) {
      const headers = tableLines[0].split("|").map((h) => h.trim()).filter(Boolean);
      const rows = tableLines.slice(2).map((r) => r.split("|").map((c) => c.trim()).filter(Boolean));
      rendered.push(
        <div key={`table-${key}`} className="my-3 overflow-x-auto rounded-lg border border-border">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="bg-muted/60">
                {headers.map((h, i) => (
                  <th key={i} className="px-3 py-2 text-left font-semibold text-foreground whitespace-nowrap">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr key={ri} className={ri % 2 === 0 ? "bg-background" : "bg-muted/20"}>
                  {row.map((cell, ci) => (
                    <td key={ci} className="px-3 py-2 text-muted-foreground">{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }
    tableLines = [];
    inTable = false;
  };

  lines.forEach((line, i) => {
    const key = String(i);

    if (line.trim().startsWith("|")) {
      if (!inTable) inTable = true;
      tableLines.push(line.trim());
      return;
    } else if (inTable) {
      flushTable(key);
    }

    if (line.startsWith("## ") || line.startsWith("### ")) {
      flushList(key);
      const text = line.replace(/^#{2,3}\s/, "");
      rendered.push(
        <h3 key={key} className="font-semibold text-foreground text-[15px] mt-4 mb-1.5 first:mt-0">
          {text}
        </h3>
      );
    } else if (line.startsWith("**") && line.endsWith("**") && !line.slice(2, -2).includes("**")) {
      flushList(key);
      rendered.push(
        <p key={key} className="font-semibold text-foreground text-sm mt-3 mb-1 first:mt-0">
          {line.slice(2, -2)}
        </p>
      );
    } else if (/^\d+\.\s/.test(line)) {
      const text = line.replace(/^\d+\.\s/, "");
      listItems.push(text);
    } else if (line.startsWith("- ") || line.startsWith("* ")) {
      const text = line.replace(/^[-*]\s/, "");
      listItems.push(text);
    } else if (line.trim() === "") {
      flushList(key);
      rendered.push(<div key={key} className="h-1" />);
    } else {
      flushList(key);
      rendered.push(
        <p
          key={key}
          className="text-sm leading-relaxed"
          dangerouslySetInnerHTML={{ __html: formatInline(line) }}
        />
      );
    }
  });

  if (inTable) flushTable("end");
  flushList("end");

  return <div className={`space-y-0.5 ${className}`}>{rendered}</div>;
}

function formatInline(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, '<code class="bg-muted px-1 py-0.5 rounded text-xs font-mono">$1</code>');
}
