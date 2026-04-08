import { useState, useRef, useEffect, useCallback } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPaperPlane,
  faRobot,
  faUser,
  faBolt,
  faClock,
  faTag,
  faShieldHalved,
  faTrash,
  faSpinner,
  faCreditCard,
  faHouse,
  faLocationDot,
  faCircleInfo,
  faRightLeft,
  faBan,
  faKey,
  faFileInvoiceDollar,
} from "@fortawesome/free-solid-svg-icons";
import { type ChatMessage, getBankingResponse, QUICK_PROMPTS } from "@/lib/api";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";

const promptIcons = [
  faCreditCard,
  faHouse,
  faLocationDot,
  faCircleInfo,
  faRightLeft,
  faBan,
  faKey,
  faFileInvoiceDollar,
];

const CATEGORY_COLORS: Record<string, string> = {
  CARD: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  LOAN: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
  ACCOUNT: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
  ATM: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300",
  FIND: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300",
  TRANSFER: "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300",
  PASSWORD: "bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-300",
  FEES: "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300",
  CONTACT: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
};

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const sendMessage = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      const userMsg: ChatMessage = {
        id: `u-${Date.now()}`,
        role: "user",
        content: trimmed,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setInput("");
      setIsLoading(true);

      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }

      try {
        const result = await getBankingResponse(trimmed);
        const botMsg: ChatMessage = {
          id: `b-${Date.now()}`,
          role: "assistant",
          content: result.response,
          intent: result.intent,
          category: result.category,
          confidence: result.confidence,
          response_time: result.response_time,
          masked_pii: result.masked_pii,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, botMsg]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            id: `err-${Date.now()}`,
            role: "assistant",
            content:
              "I apologize, but I encountered an error processing your request. Please check your backend connection and try again.",
            timestamp: new Date(),
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  };

  const clearChat = () => setMessages([]);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex flex-col h-full min-h-0">
      <div className="flex-shrink-0 flex items-center justify-between px-6 py-4 border-b border-border bg-background">
        <div>
          <h1 className="text-lg font-semibold text-foreground">Banking Assistant</h1>
          <p className="text-xs text-muted-foreground mt-0.5">Powered by Hugging Face MiniLM V6 + RAG</p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearChat}
            data-testid="button-clear-chat"
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
          >
            <FontAwesomeIcon icon={faTrash} className="text-xs" />
            Clear
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto min-h-0 px-4 py-4 space-y-4">
        {isEmpty ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4 fade-in-up">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-5">
              <FontAwesomeIcon icon={faRobot} className="text-primary text-2xl" />
            </div>
            <h2 className="text-xl font-semibold text-foreground mb-2">How can I help you today?</h2>
            <p className="text-muted-foreground text-sm max-w-sm mb-8">
              Ask me anything about banking services — cards, loans, transfers, ATMs, account management and more.
            </p>
            <div className="grid grid-cols-2 gap-2 w-full max-w-lg">
              {QUICK_PROMPTS.map((p, i) => (
                <button
                  key={p.label}
                  onClick={() => sendMessage(p.label)}
                  data-testid={`button-quick-prompt-${i}`}
                  className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl border border-border bg-card text-left text-sm text-foreground hover:border-primary/40 hover:bg-primary/5 transition-all duration-150 cursor-pointer"
                >
                  <FontAwesomeIcon icon={promptIcons[i]} className="text-primary text-xs flex-shrink-0" />
                  <span className="truncate">{p.label}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <div
                key={msg.id}
                data-testid={`msg-${msg.role}-${msg.id}`}
                className={`flex gap-3 ${msg.role === "user" ? "justify-end msg-user" : "justify-start msg-bot"}`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <FontAwesomeIcon icon={faRobot} className="text-primary text-xs" />
                  </div>
                )}

                <div className={`max-w-[80%] space-y-1.5 ${msg.role === "user" ? "items-end flex flex-col" : ""}`}>
                  <div
                    className={`rounded-2xl px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-primary text-primary-foreground rounded-tr-sm"
                        : "bg-card border border-border text-card-foreground rounded-tl-sm"
                    }`}
                  >
                    {msg.role === "user" ? (
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                    ) : (
                      <MarkdownRenderer content={msg.content} />
                    )}
                  </div>

                  {msg.role === "assistant" && (msg.intent || msg.category) && (
                    <div className="flex flex-wrap items-center gap-2 px-1">
                      {msg.category && (
                        <span
                          data-testid={`badge-category-${msg.id}`}
                          className={`inline-flex items-center gap-1.5 text-[11px] font-medium px-2 py-0.5 rounded-full ${CATEGORY_COLORS[msg.category] || "bg-muted text-muted-foreground"}`}
                        >
                          <FontAwesomeIcon icon={faTag} className="text-[9px]" />
                          {msg.category}
                        </span>
                      )}
                      {msg.confidence !== undefined && (
                        <span className="inline-flex items-center gap-1.5 text-[11px] text-muted-foreground">
                          <FontAwesomeIcon icon={faBolt} className="text-[9px] text-amber-500" />
                          {(msg.confidence * 100).toFixed(0)}% confidence
                        </span>
                      )}
                      {msg.response_time !== undefined && (
                        <span className="inline-flex items-center gap-1.5 text-[11px] text-muted-foreground">
                          <FontAwesomeIcon icon={faClock} className="text-[9px]" />
                          {msg.response_time.toFixed(2)}s
                        </span>
                      )}
                      {msg.masked_pii && (
                        <span className="inline-flex items-center gap-1.5 text-[11px] text-emerald-600 dark:text-emerald-400">
                          <FontAwesomeIcon icon={faShieldHalved} className="text-[9px]" />
                          PII masked
                        </span>
                      )}
                    </div>
                  )}

                  <p className="text-[10px] text-muted-foreground/60 px-1">
                    {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </p>
                </div>

                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0 mt-0.5">
                    <FontAwesomeIcon icon={faUser} className="text-muted-foreground text-xs" />
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3 msg-bot">
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <FontAwesomeIcon icon={faRobot} className="text-primary text-xs" />
                </div>
                <div className="bg-card border border-border rounded-2xl rounded-tl-sm px-4 py-3">
                  <div className="flex items-center gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground typing-dot" />
                    <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground typing-dot" />
                    <div className="w-1.5 h-1.5 rounded-full bg-muted-foreground typing-dot" />
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </>
        )}
      </div>

      <div className="flex-shrink-0 px-4 pb-4 pt-2 border-t border-border bg-background">
        <div className="flex items-end gap-3 bg-card border border-border rounded-2xl px-4 py-3 focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/10 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your banking needs..."
            rows={1}
            data-testid="input-chat-message"
            className="flex-1 resize-none bg-transparent outline-none text-sm text-foreground placeholder:text-muted-foreground min-h-[24px] max-h-[120px] leading-6"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isLoading}
            data-testid="button-send-message"
            className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center text-primary-foreground disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 active:scale-95 transition-all flex-shrink-0 cursor-pointer"
          >
            {isLoading ? (
              <FontAwesomeIcon icon={faSpinner} className="text-sm animate-spin" />
            ) : (
              <FontAwesomeIcon icon={faPaperPlane} className="text-sm" />
            )}
          </button>
        </div>
        <p className="text-[10px] text-muted-foreground/50 text-center mt-2">
          Press Enter to send · Shift+Enter for new line · PII is automatically detected and masked
        </p>
      </div>
    </div>
  );
}
