import React from 'react';
import OriginalBlogAuthorsListPage from '@theme-original/Blog/Pages/BlogAuthorsListPage';
import Head from '@docusaurus/Head';

const SITE_URL = 'https://equipment-python.vercel.app';
const PAGE_URL = `${SITE_URL}/blog/authors`;
const OG_IMAGE = `${SITE_URL}/img/og-social-card.png`;
const PAGE_TITLE = 'Blog Authors — Equipment';
const PAGE_DESCRIPTION =
  'Meet the authors behind Equipment, its Python project scaffolding framework, documentation, and blog.';

export default function BlogAuthorsListPage(props) {
  const authors = props.authors
    .filter((author) => author.name)
    .map((author, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      item: {
        '@type': 'Person',
        name: author.name,
        ...(author.url ? { url: author.url } : {}),
      },
    }));

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: PAGE_TITLE,
    description: PAGE_DESCRIPTION,
    url: PAGE_URL,
    mainEntity: {
      '@type': 'ItemList',
      itemListElement: authors,
    },
  };

  return (
    <>
      <OriginalBlogAuthorsListPage {...props} />

      <Head>
        <link rel="canonical" href={PAGE_URL} />
        <meta name="description" content={PAGE_DESCRIPTION} />
        <meta property="og:title" content={PAGE_TITLE} />
        <meta property="og:description" content={PAGE_DESCRIPTION} />
        <meta property="og:url" content={PAGE_URL} />
        <meta property="og:type" content="website" />
        <meta property="og:image" content={OG_IMAGE} />
        <meta property="og:image:alt" content={PAGE_TITLE} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={PAGE_TITLE} />
        <meta name="twitter:description" content={PAGE_DESCRIPTION} />
        <meta name="twitter:image" content={OG_IMAGE} />
        <meta name="twitter:image:alt" content={PAGE_TITLE} />
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      </Head>
    </>
  );
}
