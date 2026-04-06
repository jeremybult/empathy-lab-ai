import ChatWidget from '@/components/ChatWidget';
import type { Persona } from '@/components/types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

async function getPersonas(): Promise<Persona[]> {
  try {
    const response = await fetch(`${API_BASE}/api/personas`, { cache: 'no-store' });
    if (!response.ok) throw new Error('Failed to load personas');
    const data = await response.json();
    return data.personas;
  } catch {
    return [
      {
        id: 'andrea_miller',
        name: 'Andrea Miller',
        title: 'OCD Persona',
        summary: 'Represents lived experience with obsessive-compulsive disorder.',
        accent: '#7ae7c7'
      },
      {
        id: 'dr_candice_martinez',
        name: 'Dr. Candice Martinez',
        title: 'Clinical Psychologist Persona',
        summary: 'Explains ADHD and clinical perspectives in approachable terms.',
        accent: '#b2f06b'
      },
      {
        id: 'cooper_litt',
        name: 'Cooper Litt',
        title: 'College Student Persona',
        summary: 'Shares a patient-centered ADHD perspective and student experience.',
        accent: '#f1d472'
      }
    ];
  }
}

export default async function HomePage() {
  const personas = await getPersonas();

  return (
    <main className="page-shell">
      <div className="aurora aurora-a" />
      <div className="aurora aurora-b" />
      <header className="topbar glass-strip">
        <div className="brand-lockup">
          <span className="brand-mark" />
          <div>
            <strong>Empathy Lab AI</strong>
            <p>Psychology education through interactive persona dialogue</p>
          </div>
        </div>
        <nav>
          <a href="#about">About</a>
          <a href="#workflow">How It Works</a>
          <a href="#personas">Personas</a>
          <a href="#impact">Impact</a>
          <a href="#demo">Demo</a>
        </nav>
      </header>

      <section className="hero glass-panel">
        <div className="hero-copy">
          <p className="eyebrow">AI-Powered Persona Chatbots</p>
          <h1>An immersive AI interface for psychology education and empathy development.</h1>
          <p className="lead">
            Explore research-grounded personas, ask questions in real time, and present the project as a polished educational platform instead of a static research poster.
          </p>
          <div className="cta-row">
            <a className="primary-button" href="#demo">Try the Demo</a>
            <a className="ghost-button" href="#about">Explore the Project</a>
          </div>
        </div>
        <div className="hero-card glass-card">
          <p className="eyebrow">System Overview</p>
          <ul>
            <li>Voice or text question</li>
            <li>Speech recognition in the browser</li>
            <li>Python backend with persona-aware prompts</li>
            <li>Natural language response for learning and empathy practice</li>
            <li>Browser speech output to keep runtime costs low</li>
          </ul>
        </div>
      </section>

      <section id="about" className="content-grid">
        <article className="glass-panel">
          <p className="eyebrow">About the Project</p>
          <h2>Research-forward, human-centered, and built for dialogue</h2>
          <p>
            This project explores AI-driven persona chatbots as interactive educational tools for psychology students and empathy research. Instead of only reading about symptoms and diagnostic criteria, users can engage in real-time conversation with structured personas representing lived experience and clinical perspectives.
          </p>
        </article>
        <article className="glass-panel">
          <p className="eyebrow">Why it matters</p>
          <p>
            The goal is not novelty for its own sake. It is to create a more vivid, memorable, and empathic way to learn about mental health conditions, treatment approaches, and the human experience behind psychological concepts.
          </p>
        </article>
      </section>

      <section id="workflow" className="glass-panel workflow-section">
        <p className="eyebrow">How It Works</p>
        <h2>Voice, language, and persona design working together</h2>
        <div className="workflow-grid">
          {[
            ['01', 'Ask a question', 'The user starts with text or voice inside the browser.'],
            ['02', 'Interpret the prompt', 'The backend frames the conversation through the selected persona.'],
            ['03', 'Generate a response', 'A language model returns a research-oriented response when a live API key is configured.'],
            ['04', 'Deliver the experience', 'The answer appears in chat and can be spoken aloud through browser voice.']
          ].map(([step, title, copy]) => (
            <article key={step} className="workflow-card glass-card">
              <span>{step}</span>
              <h3>{title}</h3>
              <p>{copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="personas" className="glass-panel">
        <p className="eyebrow">Featured Personas</p>
        <h2>Multiple perspectives, one cohesive learning experience</h2>
        <div className="persona-grid">
          {personas.map((persona) => (
            <article key={persona.id} className="glass-card persona-preview">
              <span className="accent-dot" style={{ background: persona.accent }} />
              <h3>{persona.name}</h3>
              <p className="persona-title">{persona.title}</p>
              <p>{persona.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="impact" className="content-grid impact-grid">
        <article className="glass-panel">
          <p className="eyebrow">Research Impact</p>
          <h2>Built for classrooms, empathy studies, and public-facing demos</h2>
          <p>
            The platform can support psychology coursework, interactive classroom discussion, and future research on how dialogue-based systems influence empathic understanding.
          </p>
        </article>
        <article className="glass-panel">
          <p className="eyebrow">Future Directions</p>
          <p>
            Expand the persona library, connect richer sources, add persistent storage, and refine the web application into a durable platform for research and teaching.
          </p>
        </article>
      </section>

      <ChatWidget personas={personas} />
    </main>
  );
}
