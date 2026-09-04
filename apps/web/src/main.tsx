import React, {FormEvent, useState} from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

type Citation = {source:string; excerpt:string; score:number};
type Action = {id:string; name:string; arguments:Record<string,string>; status:string};
type Reply = {traceId:string; answer:string; citations:Citation[]; confidence:number; action?:Action; guardrail:string};
const API = import.meta.env.VITE_API_URL ?? "http://localhost:8080";

function App() {
  const [question,setQuestion]=useState("What should I do when the API has high latency?");
  const [reply,setReply]=useState<Reply|null>(null);
  const [loading,setLoading]=useState(false);
  const [execution,setExecution]=useState("");
  async function ask(event:FormEvent) {
    event.preventDefault(); setLoading(true); setReply(null); setExecution("");
    try {
      const response=await fetch(`${API}/api/chat`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({sessionId:"portfolio-demo",message:question})});
      if(!response.ok) throw new Error("The service could not be reached");
      setReply(await response.json());
    } catch(error) { setExecution(error instanceof Error?error.message:"Error inesperado"); }
    finally {setLoading(false)}
  }
  async function approve(action:Action) {
    const response=await fetch(`${API}/api/actions/${action.id}/approve`,{method:"POST"});
    const data=await response.json(); setExecution(response.ok?`Executed: ${data.result.ticket} (${data.result.severity})`:data.error);
  }
  return <main>
    <header><div className="mark">OP</div><div><p className="eyebrow">AI OPERATIONS LAB</p><h1>OpsPilot</h1></div><span className="status"><i/> All systems operational</span></header>
    <section className="hero"><p className="eyebrow">EVIDENCE-GROUNDED COPILOT</p><h2>Operational answers,<br/><em>without losing control.</em></h2><p>Search runbooks, inspect the sources, and approve every sensitive action.</p></section>
    <section className="workspace">
      <form onSubmit={ask}><label htmlFor="prompt">Ask the copilot</label><div className="input"><textarea id="prompt" value={question} onChange={e=>setQuestion(e.target.value)}/><button disabled={loading}>{loading?"Analyzing…":"Ask →"}</button></div>
      <div className="examples">Try: <button type="button" onClick={()=>setQuestion("Should I restart production first?")}>safe restart</button><button type="button" onClick={()=>setQuestion("Create an incident for critical latency")}>create incident</button></div></form>
      {reply&&<article className="result"><div className="resultHead"><span>ANSWER</span><span>{Math.round(reply.confidence*100)}% confidence</span></div><p className="answer">{reply.answer}</p>
        {reply.citations.length>0&&<div><h3>Retrieved evidence</h3><div className="citations">{reply.citations.map((c,i)=><aside key={i}><b>{c.source}</b><small>{Math.round(c.score*100)}% similarity</small><p>{c.excerpt}</p></aside>)}</div></div>}
        {reply.action&&<div className="approval"><div><b>Pending action</b><p>{reply.action.name} · {reply.action.arguments.severity}</p></div><button onClick={()=>approve(reply.action!)}>Approve and execute</button></div>}
        <footer>Trace <code>{reply.traceId}</code> · Guardrail: {reply.guardrail}</footer></article>}
      {execution&&<p className="notice">{execution}</p>}
    </section>
  </main>
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><App/></React.StrictMode>);
