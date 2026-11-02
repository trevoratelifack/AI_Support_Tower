import React from "react";
import { createRoot } from "react-dom/client";
import { Activity, AlertCircle, ArrowRight, Check, ChevronDown, CircleHelp, Clock3, FileText, Headphones, Search, ShieldCheck, Sparkles, UserRound, WalletCards, X } from "lucide-react";
import { getSubmittedTickets, runTicketWorkflow } from "./api";
import CustomerPortal from "./CustomerPortal";
import "./styles.css";

const tickets = [
  { ticket_id: "TCK-1001", customer_id: "CUS-001", subject: "Duplicate payment", category: "Billing", priority: "High", description: "I was charged twice for my subscription this month. The payment was €49 both times.", received: "10:42 AM", status: "New" },
  { ticket_id: "TCK-1002", customer_id: "CUS-002", subject: "Cancel subscription", category: "Account", priority: "Normal", description: "Please cancel my subscription at the end of this billing period.", received: "10:18 AM", status: "New" },
  { ticket_id: "TCK-1003", customer_id: "CUS-002", subject: "Payment failed", category: "Billing", priority: "High", description: "My renewal payment failed and I cannot update my card.", received: "9:56 AM", status: "Open" },
];
const stageInfo = [
  { key: "triage", title: "Triage", icon: CircleHelp },
  { key: "investigation", title: "Investigation", icon: Search },
  { key: "policy", title: "Policy", icon: ShieldCheck },
  { key: "resolution", title: "Resolution", icon: Sparkles },
];
const pretty = (s = "") => String(s).replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());
function StageDetails({ name, data }) {
  if (!data) return <p className="empty">Result will appear here when the workflow completes.</p>;
  const sets = {
    triage: [["Category", pretty(data.category)], ["Priority", pretty(data.priority)], ["Risk", pretty(data.risk_level)], ["Confidence", `${Math.round((data.confidence || 0) * 100)}%`], ["Reasoning", data.reasoning]],
    investigation: [["Customer verified", data.customer_verified ? "Yes" : "No"], ["Customer", data.customer_name || "Not found"], ["Subscription", data.subscription_plan || "Unknown"], ["Status", pretty(data.subscription_status || "Unknown")], ["Duplicate payment", data.duplicate_payment ? "Confirmed" : "Not confirmed"], ["Amount", data.duplicate_amount == null ? "—" : `${data.duplicate_amount} EUR`], ["Summary", data.investigation_summary]],
    policy: [["Policy", data.policy_title || "No policy found"], ["Eligible", data.eligible_for_refund ? "Yes" : "No"], ["Automatic action", data.automatic_action_allowed ? "Allowed" : "Not allowed"], ["Approval required", data.requires_human_approval ? "Yes" : "No"], ["Limit", data.refund_limit == null ? "—" : `${data.refund_limit} EUR`], ["Summary", data.policy_summary]],
    resolution: [["Recommended action", pretty(data.recommended_action)], ["Amount", data.amount == null ? "—" : `${data.amount} EUR`], ["Approval required", data.approval_required ? "Yes" : "No"], ["Confidence", `${Math.round((data.confidence || 0) * 100)}%`], ["Reason", data.action_reason], ["Customer response", data.customer_response_summary]],
  };
  return <dl className="result-grid">{sets[name].filter(([,v]) => v !== undefined).map(([k,v]) => <div className="result-row" key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>;
}
function App() {
  const [view, setView] = React.useState("operations");
  const [queue, setQueue] = React.useState(tickets);
  const [selected, setSelected] = React.useState(tickets[0]);
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [activeStage, setActiveStage] = React.useState("triage");
  const completed = stageInfo.filter(s => result?.[s.key]).length;
  async function refreshTicketQueue() {
    try {
      const response = await getSubmittedTickets();
      const submitted = response.tickets.map(item => ({
        ...item,
        category: item.workflow_result?.triage?.category ? pretty(item.workflow_result.triage.category) : "New",
        priority: item.workflow_result?.triage?.priority ? pretty(item.workflow_result.triage.priority) : "Normal",
        status: "Submitted",
        received: new Date(item.received_at).toLocaleString(),
      }));
      setQueue([...submitted, ...tickets]);
    } catch {
      // The dashboard remains usable with the built-in sample tickets when the API is unavailable.
    }
  }
  React.useEffect(() => { refreshTicketQueue(); }, []);
  async function run() {
    setLoading(true); setError(""); setResult(null); setActiveStage("triage");
    try { const data = await runTicketWorkflow(selected); setResult(data); setActiveStage(data.resolution ? "resolution" : "triage"); await refreshTicketQueue(); }
    catch (e) { setError(e.message || "Could not run the workflow. Check that the API is available."); }
    finally { setLoading(false); }
  }
  function choose(ticket) { setSelected(ticket); setResult(ticket.workflow_result || null); setActiveStage(ticket.workflow_result ? "resolution" : "triage"); setError(""); }
  const evidence = result ? [
    ["Customer data", result.investigation?.customer_name ? [`Verified customer: ${result.investigation.customer_name}`, `Subscription: ${result.investigation.subscription_plan || "unknown"} · ${result.investigation.subscription_status || "unknown"}`] : ["Customer record could not be verified"]],
    ["Payment history", result.investigation?.evidence || []],
    ["Ticket history", result.investigation?.relevant_previous_tickets?.map(t => `${t.id}: ${t.subject} (${t.status})`) || []],
    ["Company policy", result.policy?.evidence || []],
  ] : [];
  if (view === "customer") return <CustomerPortal onBack={() => { setView("operations"); refreshTicketQueue(); }}/>;
  return <div className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-icon"><Activity size={19}/></div><span>Northstar <b>OPS</b></span></div><nav><span className="nav-active">Operations</span><span>Customers</span><span>Knowledge</span></nav><button className="submit-ticket-link" onClick={() => setView("customer")}>Customer ticket form <ArrowRight size={14}/></button><div className="profile"><span className="online-dot"/>All systems operational <span className="avatar">AL</span></div></header>
    <main><div className="page-heading"><div><div className="eyebrow">SUPPORT OPERATIONS <span>/</span> INBOX</div><h1>Operations Control Tower</h1><p>Review incoming tickets and inspect AI findings before taking action.</p></div><div className="heading-meta"><span className="live"><i/> LIVE QUEUE</span><span>Updated just now</span></div></div>
      <div className="workspace">
        <aside className="inbox panel"><div className="panel-title"><div><h2>Ticket inbox</h2><span className="muted">{queue.length} tickets</span></div><button className="icon-button" aria-label="Inbox options" onClick={refreshTicketQueue}><ChevronDown size={17}/></button></div><div className="filter-search"><Search size={15}/><span>Search tickets</span><kbd>⌘ K</kbd></div><div className="filters"><button className="selected-filter">All <span>{queue.length}</span></button><button>Unassigned</button><button>Mine</button></div><div className="ticket-list">{queue.map((t, i) => <button className={`ticket-item ${selected.ticket_id === t.ticket_id ? "selected" : ""}`} key={`${t.ticket_id}-${i}`} onClick={() => choose(t)}><div className="ticket-line"><b>{t.ticket_id}</b><span className={t.priority === "High" ? "priority high" : "priority"}>{t.priority}</span></div><strong>{t.subject}</strong><p>{t.description}</p><div className="ticket-foot"><span>{t.category}</span><span>{i >= queue.length - tickets.length ? (i === queue.length - 3 ? "2m" : i === queue.length - 2 ? "26m" : "48m") : t.received}</span></div></button>)}</div><div className="inbox-footer"><Headphones size={15}/> Queue health <span className="health-value">Good</span></div></aside>
        <section className="main-column"><section className="ticket-detail panel"><div className="detail-top"><div><span className="ticket-id">{selected.ticket_id}</span><span className="status-pill"><i/> {selected.status}</span></div><button className="more-button">•••</button></div><h2>{selected.subject}</h2><p className="ticket-description">{selected.description}</p><div className="ticket-facts"><div><span>Customer</span><b><UserRound size={14}/>{selected.customer_id}</b></div><div><span>Received</span><b><Clock3 size={14}/>{selected.received}</b></div><div><span>Category</span><b><WalletCards size={14}/>{selected.category}</b></div><div><span>Priority</span><b><span className={`priority-dot ${selected.priority === "High" ? "red" : ""}`}/>{selected.priority}</b></div></div><div className="detail-actions"><button className="primary-button" onClick={run} disabled={loading}>{loading ? <><span className="spinner"/> Running investigation…</> : <><Sparkles size={16}/> Run AI Investigation <ArrowRight size={15}/></>}</button><span>AI recommendations require operator review</span></div>{error && <div className="error-banner"><AlertCircle size={17}/><span>{error}</span><button onClick={() => setError("")} aria-label="Dismiss"><X size={16}/></button></div>}</section>
          <section className="workflow panel"><div className="section-heading"><div><h2>Workflow</h2><p>Structured analysis across four operational stages</p></div><span className="workflow-progress">{completed} / 4 complete</span></div><div className="stage-track">{stageInfo.map((s, i) => { const Icon=s.icon; const done=Boolean(result?.[s.key]); const active=loading && i === 0; return <React.Fragment key={s.key}><button className={`stage ${done ? "done" : ""} ${active ? "running" : ""} ${activeStage === s.key ? "current" : ""}`} onClick={() => setActiveStage(s.key)}><span className="stage-icon">{done ? <Check size={16}/> : <Icon size={16}/>}</span><span className="stage-copy"><b>{s.title}</b><small>{done ? "Completed" : active ? "Running" : result ? "Waiting" : "Waiting"}</small></span></button>{i < stageInfo.length - 1 && <span className={`connector ${completed > i ? "complete" : ""}`}/>}</React.Fragment>})}</div><div className="stage-result"><div className="stage-result-head"><span>{activeStage.toUpperCase()} RESULT</span>{result?.[activeStage] && <span className="completed-label"><Check size={13}/> COMPLETED</span>}</div><StageDetails name={activeStage} data={result?.[activeStage]}/></div></section></section>
        <aside className="evidence panel"><div className="panel-title"><div><h2>Evidence</h2><span className="muted">Sources used in this analysis</span></div><FileText size={17} className="muted-icon"/></div>{result ? <div className="evidence-list">{evidence.map(([title, items], i) => <section className="evidence-group" key={title}><div className="evidence-heading"><span className={`evidence-icon tone-${i}`}><FileText size={15}/></span><b>{title}</b><span className="source-count">{items.length}</span></div>{items.length ? <ul>{items.map((item, j) => <li key={j}>{item}</li>)}</ul> : <p className="evidence-empty">No evidence found</p>}</section>)}</div> : <div className="evidence-placeholder"><div className="placeholder-icon"><FileText size={19}/></div><b>Evidence will appear here</b><p>Run an investigation to review the customer, payment, ticket, and policy sources behind the recommendation.</p><div className="source-row"><UserRound size={15}/> Customer data</div><div className="source-row"><WalletCards size={15}/> Payment history</div><div className="source-row"><FileText size={15}/> Ticket history</div><div className="source-row"><ShieldCheck size={15}/> Company policy</div></div>}<div className="evidence-note"><ShieldCheck size={14}/> Recommendations include traceable evidence</div></aside>
      </div>
      {result?.resolution && <footer className="review-bar"><div><span className="review-mark"><Check size={15}/></span><div><b>Analysis complete</b><small>Review the recommendation and evidence before responding.</small></div></div><button className="secondary-button" onClick={run}>Re-run workflow</button><button className="primary-button" onClick={() => setActiveStage("resolution")}>Review recommendation <ArrowRight size={15}/></button></footer>}
    </main>
  </div>;
}

createRoot(document.getElementById("root")).render(<React.StrictMode><App/></React.StrictMode>);
