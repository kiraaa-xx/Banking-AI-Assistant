import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBrain,
  faDatabase,
  faShieldHalved,
  faGears,
  faTerminal,
  faFileCode,
  faArrowRight,
  faCheckCircle,
  faServer,
  faNetworkWired,
  faCode,
  faArrowUpRightFromSquare,
} from "@fortawesome/free-solid-svg-icons";

const architecture = [
  {
    step: "01",
    title: "User Query",
    desc: "Customer submits a natural language banking question",
    icon: faTerminal,
    color: "text-blue-500",
    bg: "bg-blue-50 dark:bg-blue-900/20",
  },
  {
    step: "02",
    title: "Preprocessing",
    desc: "PII detection, text normalization, and query enhancement",
    icon: faShieldHalved,
    color: "text-purple-500",
    bg: "bg-purple-50 dark:bg-purple-900/20",
  },
  {
    step: "03",
    title: "Vector Search",
    desc: "FAISS similarity search across 25,545 banking embeddings",
    icon: faDatabase,
    color: "text-emerald-500",
    bg: "bg-emerald-50 dark:bg-emerald-900/20",
  },
  {
    step: "04",
    title: "RAG Pipeline",
    desc: "Top-K context retrieval + response generation with MiniLM V6",
    icon: faBrain,
    color: "text-amber-500",
    bg: "bg-amber-50 dark:bg-amber-900/20",
  },
  {
    step: "05",
    title: "Response",
    desc: "Accurate, compliant banking response delivered to the customer",
    icon: faCheckCircle,
    color: "text-cyan-500",
    bg: "bg-cyan-50 dark:bg-cyan-900/20",
  },
];

const techStack = [
  { name: "Hugging Face MiniLM V6", role: "Sentence Embeddings & Response Generation", icon: faBrain },
  { name: "FAISS Vector Database", role: "Fast Approximate Nearest Neighbor Search", icon: faDatabase },
  { name: "Python / Streamlit", role: "Backend & Original Web Interface", icon: faCode },
  { name: "React + Vite", role: "This Frontend Interface", icon: faFileCode },
  { name: "RAG Pipeline", role: "Retrieval-Augmented Generation Framework", icon: faNetworkWired },
  { name: "PII Detection Engine", role: "Regex-based Sensitive Data Masking", icon: faShieldHalved },
];

const scripts = [
  { name: "banking_assistant.py", desc: "Core assistant with embedding and RAG pipeline" },
  { name: "preprocessing_pipeline.py", desc: "Data cleaning, normalization, and PII masking" },
  { name: "vector_database.py", desc: "FAISS index creation and similarity search" },
  { name: "setup_models.py", desc: "Hugging Face model download and configuration" },
  { name: "web_interface.py", desc: "Streamlit UI with statistics and chat interface" },
  { name: "data_analysis.py", desc: "Dataset analysis and visualization generation" },
  { name: "start_system.py", desc: "System startup orchestration script" },
  { name: "demo_system.py", desc: "Demonstration and testing script" },
];

const apiEnv = [
  { key: "VITE_BACKEND_URL", desc: "Base URL of your Python backend (e.g. http://localhost:8501)", required: false },
  { key: "HUGGINGFACE_API_KEY", desc: "Your Hugging Face API key for model access (set in Python .env)", required: true },
  { key: "HUGGINGFACE_MODEL", desc: "Model name, default: sentence-transformers/all-MiniLM-L6-v2", required: false },
  { key: "VECTOR_DB_PATH", desc: "Path to FAISS vector database directory", required: false },
  { key: "PROCESSED_DATA_PATH", desc: "Path to processed_banking_dataset.csv", required: false },
];

export default function About() {
  return (
    <div className="h-full overflow-y-auto px-6 py-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="fade-in-up">
          <h1 className="text-2xl font-semibold text-foreground">About the System</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Technical architecture, system components, and setup guide
          </p>
        </div>

        <div className="bg-card border border-border rounded-2xl p-6 fade-in-up">
          <div className="flex items-center gap-2 mb-4">
            <FontAwesomeIcon icon={faBrain} className="text-primary text-sm" />
            <h2 className="font-semibold text-foreground">Project Overview</h2>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">
            This is a Final Year Project implementing an intelligent banking assistant using{" "}
            <strong className="text-foreground">Large Language Models (LLM)</strong> with{" "}
            <strong className="text-foreground">Retrieval-Augmented Generation (RAG)</strong>. The system achieves{" "}
            <strong className="text-foreground">91% overall accuracy</strong> in intent classification and response
            generation, trained on a dataset of 25,545 real banking interactions across 9 categories and 26 distinct
            customer intents. It uses Hugging Face MiniLM V6 for sentence embeddings and FAISS for efficient vector
            similarity search.
          </p>
          <a
            href="https://github.com/BipinShahi/Final-Year-Project"
            target="_blank"
            rel="noopener noreferrer"
            data-testid="link-github-repo"
            className="inline-flex items-center gap-2 mt-4 text-sm text-primary hover:underline"
          >
            <FontAwesomeIcon icon={faArrowUpRightFromSquare} className="text-xs" />
            View on GitHub
          </a>
        </div>

        <div className="bg-card border border-border rounded-2xl p-6 fade-in-up">
          <div className="flex items-center gap-2 mb-5">
            <FontAwesomeIcon icon={faGears} className="text-primary text-sm" />
            <h2 className="font-semibold text-foreground">System Architecture</h2>
          </div>
          <div className="flex flex-col sm:flex-row items-start gap-0">
            {architecture.map(({ step, title, desc, icon, color, bg }, i) => (
              <div key={step} className="flex sm:flex-col items-start sm:items-center gap-4 sm:gap-2 flex-1">
                <div className="flex sm:flex-col items-center gap-3 sm:gap-2 w-full">
                  <div className={`w-12 h-12 rounded-xl ${bg} flex items-center justify-center flex-shrink-0`}>
                    <FontAwesomeIcon icon={icon} className={`${color} text-lg`} />
                  </div>
                  {i < architecture.length - 1 && (
                    <FontAwesomeIcon
                      icon={faArrowRight}
                      className="text-muted-foreground/40 sm:hidden text-sm"
                    />
                  )}
                </div>
                <div className="sm:text-center min-w-0 flex-1">
                  <p className="text-[10px] font-medium text-muted-foreground mb-0.5">{step}</p>
                  <p className="text-sm font-semibold text-foreground">{title}</p>
                  <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">{desc}</p>
                </div>
                {i < architecture.length - 1 && (
                  <div className="hidden sm:flex items-center justify-center w-full mt-3">
                    <FontAwesomeIcon icon={faArrowRight} className="text-muted-foreground/30 text-sm" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 fade-in-up">
          <div className="bg-card border border-border rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <FontAwesomeIcon icon={faServer} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Technology Stack</h2>
            </div>
            <div className="space-y-3">
              {techStack.map(({ name, role, icon }) => (
                <div key={name} className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <FontAwesomeIcon icon={icon} className="text-primary text-xs" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-foreground">{name}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{role}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-card border border-border rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <FontAwesomeIcon icon={faFileCode} className="text-primary text-sm" />
              <h2 className="font-semibold text-foreground">Backend Scripts</h2>
            </div>
            <div className="space-y-2.5">
              {scripts.map(({ name, desc }) => (
                <div key={name} className="flex items-start gap-2.5">
                  <FontAwesomeIcon
                    icon={faCheckCircle}
                    className="text-emerald-500 text-xs mt-1 flex-shrink-0"
                  />
                  <div className="min-w-0">
                    <code className="text-xs font-mono text-foreground bg-muted px-1.5 py-0.5 rounded">{name}</code>
                    <p className="text-xs text-muted-foreground mt-0.5">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-2xl p-6 fade-in-up">
          <div className="flex items-center gap-2 mb-4">
            <FontAwesomeIcon icon={faTerminal} className="text-primary text-sm" />
            <h2 className="font-semibold text-foreground">Setup Guide</h2>
          </div>
          <div className="space-y-4 text-sm">
            {[
              {
                num: "1",
                title: "Clone Repository",
                code: `git clone https://github.com/BipinShahi/Final-Year-Project.git\ncd Final-Year-Project`,
              },
              {
                num: "2",
                title: "Install Python Dependencies",
                code: `pip install -r requirements.txt`,
              },
              {
                num: "3",
                title: "Configure Environment Variables",
                code: `# Create a .env file in the project root\nHUGGINGFACE_API_KEY=your_api_key_here\nHUGGINGFACE_MODEL=sentence-transformers/all-MiniLM-L6-v2\nVECTOR_DB_PATH=./vector_database\nPROCESSED_DATA_PATH=./processed_banking_dataset.csv`,
              },
              {
                num: "4",
                title: "Download Models",
                code: `python setup_models.py`,
              },
              {
                num: "5",
                title: "Run Data Preprocessing",
                code: `python preprocessing_pipeline.py`,
              },
              {
                num: "6",
                title: "Start the Backend System",
                code: `python start_system.py\n# Or use the batch launcher on Windows:\n# START_SYSTEM.bat`,
              },
              {
                num: "7",
                title: "Connect This Frontend (Optional)",
                code: `# Set VITE_BACKEND_URL in your frontend .env\nVITE_BACKEND_URL=http://localhost:8501\n# Then run:\nnpm run dev`,
              },
            ].map(({ num, title, code }) => (
              <div key={num} className="flex gap-4">
                <div className="w-7 h-7 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                  {num}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-foreground mb-1.5">{title}</p>
                  <pre className="bg-muted rounded-xl px-4 py-3 text-xs font-mono text-foreground overflow-x-auto leading-relaxed whitespace-pre-wrap">
                    {code}
                  </pre>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-card border border-border rounded-2xl p-6 fade-in-up">
          <div className="flex items-center gap-2 mb-4">
            <FontAwesomeIcon icon={faGears} className="text-primary text-sm" />
            <h2 className="font-semibold text-foreground">Environment Variables</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2.5 pr-4 font-semibold text-foreground">Variable</th>
                  <th className="text-left py-2.5 px-4 font-semibold text-foreground">Description</th>
                  <th className="text-left py-2.5 pl-4 font-semibold text-foreground">Required</th>
                </tr>
              </thead>
              <tbody>
                {apiEnv.map(({ key, desc, required }) => (
                  <tr
                    key={key}
                    className="border-b border-border/50 last:border-0 hover:bg-muted/20 transition-colors"
                  >
                    <td className="py-2.5 pr-4">
                      <code className="text-xs font-mono text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                        {key}
                      </code>
                    </td>
                    <td className="py-2.5 px-4 text-muted-foreground text-xs leading-relaxed">{desc}</td>
                    <td className="py-2.5 pl-4">
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                          required
                            ? "bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        {required ? "Required" : "Optional"}
                      </span>
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
