export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  intent?: string;
  category?: string;
  confidence?: number;
  response_time?: number;
  timestamp: Date;
  masked_pii?: boolean;
}

export interface BankingStats {
  total_records: number;
  categories: number;
  intents: number;
  accuracy: number;
  intent_accuracy: number;
  retrieval_accuracy: number;
  generation_accuracy: number;
}

export interface CategoryData {
  name: string;
  count: number;
  percentage: number;
  color: string;
}

export interface IntentData {
  name: string;
  count: number;
  category: string;
}

export const MOCK_STATS: BankingStats = {
  total_records: 25545,
  categories: 9,
  intents: 26,
  accuracy: 91,
  intent_accuracy: 92,
  retrieval_accuracy: 89,
  generation_accuracy: 91,
};

export const CATEGORY_DATA: CategoryData[] = [
  { name: "CARD", count: 5980, percentage: 23.4, color: "#3b82f6" },
  { name: "LOAN", count: 5954, percentage: 23.3, color: "#8b5cf6" },
  { name: "ACCOUNT", count: 2994, percentage: 11.7, color: "#10b981" },
  { name: "FIND", count: 1998, percentage: 7.8, color: "#f59e0b" },
  { name: "CONTACT", count: 1997, percentage: 7.8, color: "#ef4444" },
  { name: "TRANSFER", count: 1992, percentage: 7.8, color: "#06b6d4" },
  { name: "ATM", count: 1983, percentage: 7.8, color: "#84cc16" },
  { name: "PASSWORD", count: 1700, percentage: 6.7, color: "#f97316" },
  { name: "FEES", count: 947, percentage: 3.7, color: "#ec4899" },
];

export const TOP_INTENTS: IntentData[] = [
  { name: "activate_card", count: 1000, category: "CARD" },
  { name: "find_branch", count: 1000, category: "FIND" },
  { name: "check_recent_transactions", count: 999, category: "ACCOUNT" },
  { name: "human_agent", count: 999, category: "CONTACT" },
  { name: "close_account", count: 999, category: "ACCOUNT" },
  { name: "customer_service", count: 998, category: "CONTACT" },
  { name: "find_ATM", count: 998, category: "ATM" },
  { name: "block_card", count: 998, category: "CARD" },
  { name: "activate_card_international", count: 997, category: "CARD" },
  { name: "apply_for_mortgage", count: 997, category: "LOAN" },
];

export const QUICK_PROMPTS = [
  { label: "Activate my card", category: "CARD" },
  { label: "Apply for a mortgage", category: "LOAN" },
  { label: "Find nearest ATM", category: "ATM" },
  { label: "Check account balance", category: "ACCOUNT" },
  { label: "Transfer funds", category: "TRANSFER" },
  { label: "Block my card", category: "CARD" },
  { label: "Reset my password", category: "PASSWORD" },
  { label: "Check transfer fees", category: "FEES" },
];

const RESPONSES: Record<string, { intent: string; category: string; confidence: number; response: string }> = {
  activate: {
    intent: "activate_card",
    category: "CARD",
    confidence: 0.94,
    response: `To activate your credit or debit card, you have several convenient options:

**Phone Activation**
Call the number on the back of your card and follow the automated prompts. You will need your card number and personal identification.

**Online Banking**
Log in to your online banking portal, navigate to Card Services, and select "Activate Card."

**Mobile App**
Open the banking app, tap "Card Management," then "Activate Card" and follow the on-screen steps.

**In-Branch**
Visit any branch with a valid photo ID for instant activation.

Once activated, your card will be ready for purchases, ATM withdrawals, and online transactions. Is there anything else I can help you with?`,
  },
  mortgage: {
    intent: "apply_for_mortgage",
    category: "LOAN",
    confidence: 0.89,
    response: `I can guide you through our mortgage application process.

**Required Documents**
- Proof of income (pay stubs, W-2s, or 2 years of tax returns)
- Bank statements (last 3–6 months)
- Government-issued photo ID
- Employment verification letter

**Application Steps**
1. **Pre-qualification** — Get an estimate of your borrowing capacity
2. **Full Application** — Complete the mortgage application
3. **Document Submission** — Submit all required documents
4. **Processing** — Our team reviews your application (3–5 business days)
5. **Approval & Closing** — Receive approval and schedule closing

**Current Rates**
Competitive rates starting from **6.5% APR** for qualified borrowers. Both fixed and adjustable-rate options are available.

Would you like to connect with a mortgage specialist?`,
  },
  atm: {
    intent: "find_ATM",
    category: "ATM",
    confidence: 0.92,
    response: `Here are the easiest ways to find an ATM near you:

**Mobile App**
Tap "Find ATM" on the home screen for a real-time map of nearby ATMs.

**Website**
Use our ATM Locator tool — enter your zip code or allow location access.

**Phone Banking**
Call our 24/7 line and ask for nearby ATM locations.

**Our ATMs Offer**
- Cash withdrawals and deposits
- Balance inquiries and mini-statements
- Fund transfers between accounts
- PIN changes

Our network includes over **50,000 fee-free locations** nationwide. Is there a specific area you are looking for?`,
  },
  block: {
    intent: "block_card",
    category: "CARD",
    confidence: 0.96,
    response: `If your card has been lost, stolen, or compromised, block it immediately:

**Immediate Actions**
1. **Mobile App** — Go to Card Services > Block/Freeze Card. Takes effect instantly.
2. **Online Banking** — Navigate to Card Management and select "Block Card."
3. **Phone Banking** — Call our 24/7 hotline to block your card right away.

**What Happens Next**
- All transactions on the blocked card will be declined immediately
- Your funds are fully safe and accessible via other means
- A replacement card will arrive within 5–7 business days

**Dispute Unauthorized Transactions**
Report any unauthorized charges through the app or by calling our fraud hotline. We offer full fraud protection coverage.

Please act quickly — time is critical in preventing further unauthorized use!`,
  },
  transfer: {
    intent: "transfer_funds",
    category: "TRANSFER",
    confidence: 0.91,
    response: `Here is everything about fund transfers:

**Transfer Types & Fees**

| Type | Timeframe | Fee |
|------|-----------|-----|
| Same-bank transfer | Instant | Free |
| ACH transfer | 1–3 business days | Free |
| Wire (domestic) | Same day | $25 |
| Wire (international) | 1–5 business days | $45 |

**How to Transfer**
1. Log in to the app or online portal
2. Select "Transfer Money"
3. Choose source and destination accounts
4. Enter amount and confirm

**Daily Limits**
- ACH: $10,000/day
- Wire: $50,000/day

Would you like to set up a one-time or recurring transfer?`,
  },
  password: {
    intent: "reset_password",
    category: "PASSWORD",
    confidence: 0.93,
    response: `For account security, here is how to reset your password or PIN:

**Online Banking Password**
1. Click "Forgot Password" on the login page
2. Enter your registered email address
3. Check your email for a secure reset link (valid 15 minutes)
4. Follow the link and create a new password

**Mobile Banking PIN**
1. Tap "Forgot PIN" on the app login screen
2. Verify your identity via biometrics or OTP
3. Set a new 4–6 digit PIN

**Security Tips**
- Use letters, numbers, and special characters
- Never share your credentials with anyone, including bank staff

If you believe your account has been compromised, please call our fraud hotline immediately.`,
  },
  fee: {
    intent: "check_fees",
    category: "FEES",
    confidence: 0.88,
    response: `Here is an overview of our standard fees:

**Account Fees**
- Checking account: Free (with $500 minimum balance, otherwise $12/month)
- Savings account: Free
- Overdraft fee: $35 per transaction

**Transfer Fees**
- Domestic wire: $25 outgoing / $15 incoming
- International wire: $45 outgoing / $15 incoming
- ACH transfers: Free

**ATM Fees**
- Our network ATMs: Free
- Out-of-network: $2.50 per transaction

**Card Fees**
- Debit card: Free
- Credit card annual fee: $0–$95 depending on card tier
- Foreign transaction fee: 3%

Would you like details on a specific fee?`,
  },
  balance: {
    intent: "check_recent_transactions",
    category: "ACCOUNT",
    confidence: 0.90,
    response: `Check your balance and transaction history through multiple channels:

**Mobile App**
Your balance appears on the home screen. Tap any account for full transaction history with date, amount, and category filters.

**Online Banking**
Navigate to "My Accounts" to view balances and download statements (PDF or CSV).

**Phone Banking**
Call our 24/7 automated system — press 1 for checking, press 2 for savings.

**ATM**
Select "Balance Inquiry" at any ATM — free at our network locations.

**Setting Up Alerts**
Enable real-time transaction alerts in the app to be notified of every transaction instantly.

Is there anything specific about your account you need help with?`,
  },
  branch: {
    intent: "find_branch",
    category: "FIND",
    confidence: 0.91,
    response: `Here is how to find a branch near you:

**Branch Locator**
- **Mobile App** — Tap "Find Branch" to see nearby branches on a map with hours
- **Website** — Use our Branch Locator tool and enter your location
- **Phone** — Call our 24/7 helpline for branch information

**Branch Services**
- Account opening and management
- Loan and mortgage applications
- Safe deposit boxes
- Foreign currency exchange
- Notary services

**Hours**
Most branches are open Monday–Friday 9am–5pm, and Saturday 9am–1pm. Some locations have extended hours.

Is there a specific service you need at a branch?`,
  },
};

export async function getBankingResponse(query: string): Promise<{
  response: string;
  intent: string;
  category: string;
  confidence: number;
  response_time: number;
  masked_pii: boolean;
}> {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const startTime = Date.now();

  if (backendUrl) {
    try {
      const res = await fetch(`${backendUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }),
      });
      if (res.ok) {
        const data = await res.json();
        return {
          intent: "GENERAL",
          category: "GENERAL",
          confidence: 1.0,
          ...data,
          response_time: (Date.now() - startTime) / 1000,
        };
      }
    } catch {
      // Fall through to mock
    }
  }

  await new Promise((r) => setTimeout(r, 800 + Math.random() * 600));
  const q = query.toLowerCase();

  let key = "balance";
  if (q.includes("activate") && q.includes("card")) key = "activate";
  else if (q.includes("mortgage") || q.includes("loan")) key = "mortgage";
  else if (q.includes("atm") || q.includes("cash machine")) key = "atm";
  else if (q.includes("block") || q.includes("freeze")) key = "block";
  else if (q.includes("transfer") || q.includes("send money")) key = "transfer";
  else if (q.includes("password") || q.includes("pin") || q.includes("reset")) key = "password";
  else if (q.includes("fee") || q.includes("charge") || q.includes("cost")) key = "fee";
  else if (q.includes("balance") || q.includes("statement") || q.includes("transaction")) key = "balance";
  else if (q.includes("branch") || q.includes("location") || q.includes("near")) key = "branch";

  const hit = RESPONSES[key];
  return {
    ...hit,
    response_time: (Date.now() - startTime) / 1000,
    masked_pii: /\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}/.test(query),
  };
}
