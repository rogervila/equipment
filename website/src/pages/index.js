import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Head from '@docusaurus/Head';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroBadge}>
          <span>Python 3.13 – 3.15 Ready</span>
          <span>•</span>
          <span>FastMCP &amp; FastAPI Supported</span>
        </div>
        <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <p className={styles.heroDescription}>
          A Python scaffolding framework that gives your application an immediate,
          production-ready structure with configuration, dependency injection, logging,
          SQLAlchemy, queues, scheduling, storage, FastAPI, and FastMCP servers.
        </p>
        <div className={styles.terminalSnippet}>
          <span className={styles.terminalPrompt}>$</span>
          <span className={styles.terminalCommand}>pip install equipment &amp;&amp; equipment new my-app</span>
        </div>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/getting-started/installation">
            Get Started
          </Link>
          <Link
            className={clsx('button button--outline button--secondary button--lg', styles.heroButtonSecondary)}
            to="/docs/intro">
            Documentation
          </Link>
          <Link
            className={clsx('button button--outline button--secondary button--lg', styles.heroButtonSecondary)}
            href="https://github.com/rogervila/equipment">
            GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

function QuickStartSection() {
  return (
    <section className={styles.quickstartSection}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2>From Zero to Running in Minutes</h2>
          <p>Scaffold a modular application and choose only the entry points you need.</p>
        </div>
        <div className="row">
          <div className="col col--4 margin-bottom--lg">
            <div className={styles.stepCard}>
              <div className={styles.stepNumber}>1</div>
              <h3 className={styles.stepTitle}>Scaffold Your App</h3>
              <p className={styles.stepDesc}>
                Create a ready-to-run project with a complete layout and dependency configuration.
              </p>
              <pre className={styles.codeBox}>
                <code>
                  <span className={styles.codeComment}># Install Equipment CLI</span>{'\n'}
                  pip install equipment{'\n\n'}
                  <span className={styles.codeComment}># Scaffold new project</span>{'\n'}
                  equipment new my-app{'\n\n'}
                  <span className={styles.codeComment}># Install app dependencies</span>{'\n'}
                  cd my-app &amp;&amp; pip install .
                </code>
              </pre>
            </div>
          </div>
          <div className="col col--4 margin-bottom--lg">
            <div className={styles.stepCard}>
              <div className={styles.stepNumber}>2</div>
              <h3 className={styles.stepTitle}>Run Any Entry Point</h3>
              <p className={styles.stepDesc}>
                Execute scripts, web servers, background workers, or AI MCP servers seamlessly.
              </p>
              <pre className={styles.codeBox}>
                <code>
                  <span className={styles.codeComment}># Run script &amp; services</span>{'\n'}
                  python main.py{'\n\n'}
                  <span className={styles.codeComment}># Serve FastAPI web API</span>{'\n'}
                  python web.py{'\n\n'}
                  <span className={styles.codeComment}># FastMCP server for AI</span>{'\n'}
                  python mcpserver.py
                </code>
              </pre>
            </div>
          </div>
          <div className="col col--4 margin-bottom--lg">
            <div className={styles.stepCard}>
              <div className={styles.stepNumber}>3</div>
              <h3 className={styles.stepTitle}>Test &amp; Compile</h3>
              <p className={styles.stepDesc}>
                Verify standard unittests and compile code into bytecode distribution assets.
              </p>
              <pre className={styles.codeBox}>
                <code>
                  <span className={styles.codeComment}># Run unittests</span>{'\n'}
                  python -m unittest discover -s tests{'\n\n'}
                  <span className={styles.codeComment}># Compile bytecode distribution</span>{'\n'}
                  equipment compile dist{'\n\n'}
                  <span className={styles.codeComment}># Run compiled app</span>{'\n'}
                  python dist/main.pyc
                </code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CtaSection() {
  return (
    <section className={styles.ctaBanner}>
      <div className="container">
        <h2>Ready to Build Your Next Python Project?</h2>
        <p>
          Skip boilerplate wiring and start with solid infrastructure, testing, and modern integrations.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/getting-started/installation">
            Quick Start Guide
          </Link>
          <Link
            className="button button--outline button--primary button--lg"
            to="/docs/examples/mcp">
            MCP Server Guide
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} - ${siteConfig.tagline}`}
      description="Equipment is a Python project scaffolding framework for building applications with configuration, dependency injection, logging, database access, queues, scheduling, storage, FastAPI serving, and FastMCP.">
      <Head>
        <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon-16x16.png" />
        <link rel="manifest" href="/img/site.webmanifest" />
        <link rel="mask-icon" href="/img/safari-pinned-tab.svg" color="#5bbad5" />
        <meta name="msapplication-TileColor" content="#00aba9" />
        <meta name="theme-color" content="#ffffff" />
      </Head>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <QuickStartSection />
        <CtaSection />
      </main>
    </Layout>
  );
}
