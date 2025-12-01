// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
	title: "Equipment",
	tagline: "The root of your next python project",
	url: "https://equipment-python.vercel.app",
	baseUrl: "/",
	onBrokenLinks: "throw",
	onBrokenMarkdownLinks: "warn",
	favicon: "img/favicon.ico",
	organizationName: "rogervila", // Usually your GitHub org/user name.
	projectName: "equipment", // Usually your repo name.

	presets: [
		[
			"classic",
			/** @type {import('@docusaurus/preset-classic').Options} */
			({
				docs: {
					sidebarPath: require.resolve("./sidebars.js"),
					// Please change this to your repo.
					editUrl: "https://github.com/rogervila/equipment/tree/main/website/",
				},
				blog: {
					showReadingTime: true,
					// Please change this to your repo.
					editUrl: "https://github.com/rogervila/equipment/tree/main/website/",
				},
				theme: {
					customCss: require.resolve("./src/css/custom.css"),
				},
			}),
		],
	],

	// Waiting for this fix: https://github.com/cmfcmf/docusaurus-search-local/issues/234
	// "@cmfcmf/docusaurus-search-local": "^1.2.0",
	// plugins: [require.resolve("@cmfcmf/docusaurus-search-local")],

	themeConfig:
		/** @type {import('@docusaurus/preset-classic').ThemeConfig} */
		({
			navbar: {
				title: "Equipment",
				logo: {
					alt: "Equipment Logo",
					src: "img/logo.svg",
				},
				items: [
					{
						type: "doc",
						docId: "intro",
						position: "left",
						label: "Docs",
					},
					{ to: "/blog", label: "Blog", position: "left" },
					{
						href: "https://equipment-python.vercel.app/llms.txt",
						label: "LLMS.txt",
						position: "left",
					},
					{
						href: "https://pypi.org/project/equipment",
						label: "PyPI",
						position: "right",
					},
					{
						href: "https://github.com/rogervila/equipment",
						label: "GitHub",
						position: "right",
					},
				],
			},
			footer: {
				style: "dark",
				links: [
					{
						title: "Docs",
						items: [
							{
								label: "Docs",
								to: "/docs/intro",
							},
						],
					},
					{
						title: "Community",
						items: [
							// {
							//   label: 'Stack Overflow',
							//   href: 'https://stackoverflow.com/questions/tagged/equipment',
							// },
							// {
							//   label: 'Discord',
							//   href: 'https://discordapp.com/invite/docusaurus',
							// },
							{
								label: "X",
								href: "https://x.com/_rogervila",
							},
						],
					},
					{
						title: "More",
						items: [
							{
								label: "Blog",
								to: "/blog",
							},
							{
								label: "GitHub",
								href: "https://github.com/rogervila/equipment",
							},
						],
					},
				],
				copyright: `Copyright © ${new Date().getFullYear()} Roger Vilà`,
			},
			prism: {
				theme: lightCodeTheme,
				darkTheme: darkCodeTheme,
			},
		}),
};

module.exports = config;
