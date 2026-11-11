/**
 * Swizzle wrapper: DocItem/Layout
 *
 * Injects per-doc-page SEO metadata:
 *   - Canonical URL
 *   - Open Graph tags (og:title, og:description, og:url, og:type, og:image)
 *   - Twitter / X Card tags
 *   - JSON-LD TechArticle structured data
 *
 * All rendering is delegated to the original @theme-original/DocItem/Layout
 * so visual output is unchanged.
 */
import React from 'react';
import OriginalDocItemLayout from '@theme-original/DocItem/Layout';
import Head from '@docusaurus/Head';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

const SITE_URL = 'https://equipment-python.vercel.app';
const OG_IMAGE = `${SITE_URL}/img/og-social-card.png`;
const SITE_NAME = 'Equipment';

export default function DocItemLayout(props) {
  const { metadata } = useDoc();

  const {
    title,
    description,
    slug,
    frontMatter,
  } = metadata;

  // Build canonical URL.  slug starts with "/" so no extra separator needed.
  const canonicalUrl = `${SITE_URL}/docs${slug}`;

  // Allow per-doc og:image override via frontmatter `image:` field.
  const pageImage = frontMatter.image
    ? new URL(frontMatter.image, SITE_URL).href
    : OG_IMAGE;

  // Page title includes the site name suffix for social sharing.
  const socialTitle = `${title} — ${SITE_NAME}`;

  // ---- TechArticle JSON-LD ----
  const techArticleJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: title,
    description: description || `${title} — Equipment documentation`,
    url: canonicalUrl,
    image: pageImage,
    isPartOf: {
      '@type': 'WebSite',
      name: SITE_NAME,
      url: SITE_URL,
    },
    about: {
      '@type': 'SoftwareApplication',
      name: SITE_NAME,
      url: SITE_URL,
    },
    author: {
      '@type': 'Person',
      name: 'Roger Vilà',
      url: 'https://github.com/rogervila',
    },
    publisher: {
      '@type': 'Person',
      name: 'Roger Vilà',
      url: 'https://github.com/rogervila',
    },
    inLanguage: 'en',
  };

  return (
    <>
      <Head>
        {/* Canonical URL */}
        <link rel="canonical" href={canonicalUrl} />

        {/* Open Graph — per doc page */}
        <meta property="og:title" content={socialTitle} />
        <meta property="og:description" content={description || `${title} — Equipment documentation`} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:type" content="article" />
        <meta property="og:image" content={pageImage} />
        <meta property="og:image:alt" content={`${title} — Equipment`} />

        {/* Twitter / X Card — per doc page */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={socialTitle} />
        <meta name="twitter:description" content={description || `${title} — Equipment documentation`} />
        <meta name="twitter:image" content={pageImage} />
        <meta name="twitter:image:alt" content={`${title} — Equipment`} />

        {/* JSON-LD: TechArticle */}
        <script type="application/ld+json">
          {JSON.stringify(techArticleJsonLd)}
        </script>
      </Head>

      <OriginalDocItemLayout {...props} />
    </>
  );
}
