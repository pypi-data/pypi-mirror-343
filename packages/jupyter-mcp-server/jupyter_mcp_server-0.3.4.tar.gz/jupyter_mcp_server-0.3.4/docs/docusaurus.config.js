/*
 * Copyright (c) 2023-2024 Datalayer, Inc.
 *
 * BSD 3-Clause License
 */

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: '🪐 ✨ Jupyter MCP Server documentation',
  tagline: 'Tansform your Notebooks into an interactive, AI-powered workspace that adapts to your needs!',
  url: 'https://datalayer.io',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'datalayer', // Usually your GitHub org/user name.
  projectName: 'jupyter-mcp-server', // Usually your repo name.
  markdown: {
    mermaid: true,
  },
  plugins: [
    '@docusaurus/theme-live-codeblock',
    'docusaurus-lunr-search',
  ],
  themes: [
    '@docusaurus/theme-mermaid',
  ],
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
    },
    navbar: {
      title: 'Jupyter MCP Server Docs',
      logo: {
        alt: 'Datalayer Logo',
        src: 'img/datalayer/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'index',
          position: 'left',
          label: 'Overview',
        },
        {
          href: 'https://www.linkedin.com/company/datalayer',
          position: 'right',
          className: 'header-linkedin-link',
          'aria-label': 'LinkedIn',
        },
        {
          href: 'https://bsky.app/profile/datalayer.io',
          position: 'right',
          className: 'header-bluesky-link',
          'aria-label': 'Bluesky',
        },
        {
          href: 'https://github.com/datalayer/jupyter-mcp-server',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub',
        },
        {
          href: 'https://datalayer.io',
          position: 'right',
          className: 'header-datalayer-io-link',
          'aria-label': 'Datalayer IO',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Jupyter MCP Server',
              to: '/docs',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/datalayer',
            },
            {
              label: 'Bluesky',
              href: 'https://assets.datalayer.tech/logos-social-grey/youtube.svg',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/datalayer',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Datalayer',
              href: 'https://datalayer.io',
            },
            {
              label: 'Datalayer Docs',
              href: 'https://docs.datalayer.app',
            },
            {
              label: 'Datalayer Tech',
              href: 'https://datalayer.tech',
            },
            {
              label: 'Datalayer Guide',
              href: 'https://datalayer.guide',
            },
            {
              label: 'Datalayer Blog',
              href: 'https://datalayer.blog',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Datalayer, Inc.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/datalayer/jupyter-mcp-server/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
