import React from "react";
import { ArrowLeft, ArrowRight, CheckCircle2, CircleHelp, Clock3, Headphones, LoaderCircle, Send, ShieldCheck } from "lucide-react";
import { runTicketWorkflow } from "./api";
import "./customer.css";

export default function CustomerPortal({ onBack }) {
  const [form, setForm] = React.useState({ customer_id: "", subject: "", description: "" });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [submittedTicket, setSubmittedTicket] = React.useState(null);

  function update(event) {
    setForm(current => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    const ticket = {
      ...form,
      ticket_id: `TCK-${Date.now().toString().slice(-7)}`,
    };
    try {
      const response = await runTicketWorkflow(ticket);
      setSubmittedTicket(response);
    } catch (err) {
      setError(err.message || "We couldn't submit your request. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function startAnother() {
    setForm({ customer_id: "", subject: "", description: "" });
    setSubmittedTicket(null);
    setError("");
  }

  return <div className="customer-page">
    <header className="customer-topbar">
      <a className="customer-brand" href="#home" onClick={event => { event.preventDefault(); onBack(); }}>
        <span className="customer-brand-icon"><Headphones size={18}/></span>
        <span>Northstar <b>SUPPORT</b></span>
      </a>
      <button className="customer-ops-link" onClick={onBack}><ArrowLeft size={15}/> Operations view</button>
    </header>

    <main className="customer-main">
      <div className="customer-intro">
        <div className="customer-eyebrow"><span/> CUSTOMER SUPPORT</div>
        <h1>How can we help?</h1>
        <p>Tell us what happened and our support team will take a look.</p>
      </div>

      {submittedTicket ? <section className="submission-success" role="status">
        <div className="success-icon"><CheckCircle2 size={25}/></div>
        <h2>Your request is in the queue</h2>
        <p>Your support request was submitted for review. Keep this reference number for your records.</p>
        <div className="reference-box"><span>REFERENCE NUMBER</span><strong>{submittedTicket.ticket_id}</strong></div>
        <div className="success-expectation"><Clock3 size={16}/><span>A support specialist can use this reference when reviewing your request.</span></div>
        <div className="success-actions"><button className="customer-secondary" onClick={startAnother}>Submit another request</button><button className="customer-primary" onClick={onBack}>Return to operations <ArrowRight size={15}/></button></div>
      </section> : <section className="customer-form-card">
        <div className="form-card-heading"><div className="form-heading-icon"><CircleHelp size={18}/></div><div><h2>Submit a support request</h2><p>Fields marked with <span>*</span> are required.</p></div></div>
        <form onSubmit={submit}>
          <label htmlFor="customer_id">Customer ID <span>*</span></label>
          <input id="customer_id" name="customer_id" value={form.customer_id} onChange={update} placeholder="e.g. CUS-001" required autoComplete="off"/>
          <p className="field-hint">For this demo, use CUS-001 or CUS-002. Enter the ID associated with your account.</p>

          <label htmlFor="subject">What do you need help with? <span>*</span></label>
          <input id="subject" name="subject" value={form.subject} onChange={update} placeholder="Briefly describe the issue" required maxLength={160}/>

          <label htmlFor="description">Tell us more <span>*</span></label>
          <textarea id="description" name="description" value={form.description} onChange={update} placeholder="Include any details that will help us understand and resolve your issue." required minLength={8} maxLength={3000} rows={6}/>
          <div className="form-bottom"><span>{form.description.length}/3000</span><span>Your information is used to review this support request.</span></div>

          {error && <div className="customer-error" role="alert">{error}</div>}
          <button className="customer-primary submit-button" type="submit" disabled={loading}>
            {loading ? <><LoaderCircle className="loading-icon" size={16}/> Sending request…</> : <>Submit request <Send size={15}/></>}
          </button>
        </form>
      </section>}

      <div className="customer-assurance"><ShieldCheck size={15}/><span>AI recommendations support the team’s review. No account changes happen automatically.</span></div>
      <div className="customer-help">Please include your reference number if you follow up with support.</div>
    </main>
  </div>;
}
