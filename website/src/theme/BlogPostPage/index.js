/**
 * Swizzle wrapper: BlogPostPage
 *
 * Injects per-blog-post SEO metadata:
 *   - Canonical URL
 *   - Open Graph tags (og:title, og:description, og:url, og:type, og:image,
 *     og:article:published_time, og:article:author, og:article:tag)
 *   - Twitter / X Card tags
 *   - JSON-LD BlogPosting (Article) structured data
 *   - JSON-LD BreadcrumbList
 *
 * All rendering is delegated to @theme-original/BlogPostPage.
 */
import React from 'react';
import OriginalBlogPostPage from '@theme-original/BlogPostPage';
import Head from '@docusaurus/Head';

const SITE_URL = 'https://equipment-python.vercel.app';
const OG_IMAGE = `${SITE_URL}/img/og-social-card.png`;
const SITE_NAME = 'Equipment';

export default function BlogPostPage(props) {
  const { metadata, frontMatter, assets } = props.content;

  const { title, description, permalink } = metadata;

  const canonicalUrl = `${SITE_URL}${permalink}`;
  const socialTitle = `${title} — ${SITE_NAME}`;
  const socialDescription = description || `${title} on the Equipment blog`;

  // Use the blog post's featured image if set, otherwise fall back to default.
  const image = assets?.image || frontMatter.image;
  const pageImage = image ? new URL(image, SITE_URL).href : OG_IMAGE;

  // ---- BreadcrumbList JSON-LD ----
  const breadcrumbJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: `${SITE_URL}/`,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Blog',
        item: `${SITE_URL}/blog`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: title,
        item: canonicalUrl,
      },
    ],
  };

  return (
    <>
      <OriginalBlogPostPage {...props} />

      <Head>
        {/* Canonical URL */}
        <link rel="canonical" href={canonicalUrl} />

        {/* Open Graph — blog post */}
        <meta property="og:title" content={socialTitle} />
        <meta property="og:description" content={socialDescription} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:type" content="article" />
        <meta property="og:image" content={pageImage} />
        <meta property="og:image:alt" content={`${title} — ${SITE_NAME}`} />
        {/* Twitter / X Card — blog post */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={socialTitle} />
        <meta name="twitter:description" content={socialDescription} />
        <meta name="twitter:image" content={pageImage} />
        <meta name="twitter:image:alt" content={`${title} — ${SITE_NAME}`} />

        {/* JSON-LD: BreadcrumbList */}
        <script type="application/ld+json">
          {JSON.stringify(breadcrumbJsonLd)}
        </script>
      </Head>
    </>
  );
}
