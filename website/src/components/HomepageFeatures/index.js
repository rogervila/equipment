import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

function TerminalIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 17 10 11 4 5" />
      <line x1="12" y1="19" x2="20" y2="19" />
    </svg>
  );
}

function SlidersIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="4" y1="21" x2="4" y2="14" />
      <line x1="4" y1="10" x2="4" y2="3" />
      <line x1="12" y1="21" x2="12" y2="12" />
      <line x1="12" y1="8" x2="12" y2="3" />
      <line x1="20" y1="21" x2="20" y2="16" />
      <line x1="20" y1="12" x2="20" y2="3" />
      <line x1="1" y1="14" x2="7" y2="14" />
      <line x1="9" y1="8" x2="15" y2="8" />
      <line x1="17" y1="16" x2="23" y2="16" />
    </svg>
  );
}

function DatabaseIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
    </svg>
  );
}

function ClockIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function SparklesIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z" />
      <path d="M19 4v4" />
      <path d="M21 6h-4" />
    </svg>
  );
}

function PackageIcon() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="16.5" y1="9.4" x2="7.5" y2="4.21" />
      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
      <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
      <line x1="12" y1="22.08" x2="12" y2="12" />
    </svg>
  );
}

const FeatureList = [
  {
    title: 'Instant Scaffolding',
    Icon: TerminalIcon,
    description: (
      <>
        Scaffold production-ready Python projects in seconds with <code>equipment new</code>.
        Includes a lightweight dependency injection container and standardized project layout.
      </>
    ),
  },
  {
    title: 'Unified Configuration & Logging',
    Icon: SlidersIcon,
    description: (
      <>
        Load YAML, JSON, and INI configuration files with environment variable interpolation
        (<code>${'{VAR:default}'}</code>) alongside structured, multi-channel logging.
      </>
    ),
  },
  {
    title: 'Database & Storage',
    Icon: DatabaseIcon,
    description: (
      <>
        Pre-configured SQLAlchemy database engine and session management with Alembic migrations,
        plus unified storage drivers for local disk and AWS S3.
      </>
    ),
  },
  {
    title: 'Queues & Task Scheduling',
    Icon: ClockIcon,
    description: (
      <>
        Process background jobs with sync and Redis queue workers,
        and run cron-style periodic tasks with the built-in scheduler.
      </>
    ),
  },
  {
    title: 'FastAPI & FastMCP Ready',
    Icon: SparklesIcon,
    description: (
      <>
        Serve web APIs with <strong>FastAPI</strong> and expose application services to AI assistants
        like Claude Code, Cursor, and VS Code with <strong>FastMCP</strong> (Model Context Protocol).
      </>
    ),
  },
  {
    title: 'Tested & Cross-Platform',
    Icon: PackageIcon,
    description: (
      <>
        Bytecode compilation via <code>equipment compile</code> for distribution. Full support
        for Python 3.13, 3.14, and 3.15 across Linux, macOS, and Windows with standard <code>unittest</code>.
      </>
    ),
  },
];

function Feature({ Icon, title, description }) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <div className={styles.featureCard}>
        <div className={styles.iconWrapper}>
          <Icon />
        </div>
        <h3 className={styles.featureTitle}>{title}</h3>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
