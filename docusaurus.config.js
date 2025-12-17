// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'A Comprehensive Guide to Embodied Intelligence',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<org-name>/<repo-name>/'
  baseUrl: '/physical-ai-humanoid-robotics-book-q4/',

  // GitHub pages deployment config.
  organizationName: 'your-organization', // Usually your GitHub org/user name.
  projectName: 'physical-ai-humanoid-robotics-book-q4', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username/physical-ai-humanoid-robotics-book-q4/tree/main/',
        },
        blog: false, // Disable blog for textbook format
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'textbookSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/your-username/physical-ai-humanoid-robotics-book-q4',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'Introduction to Physical AI',
                to: '/docs/chapter-1-introduction-to-physical-ai',
              },
              {
                label: 'Humanoid Robotics Basics',
                to: '/docs/chapter-2-basics-of-humanoid-robotics',
              },
              {
                label: 'ROS 2 Fundamentals',
                to: '/docs/chapter-3-ros-2-fundamentals',
              },
              {
                label: 'Digital Twin Simulation',
                to: '/docs/chapter-4-digital-twin-simulation',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/physical-ai-humanoid-robotics-book-q4',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Report Issues',
                href: 'https://github.com/your-username/physical-ai-humanoid-robotics-book-q4/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'json', 'yaml', 'dockerfile'],
      },
      algolia: {
        // Optional: Add search if needed
        appId: process.env.ALGOLIA_APP_ID,
        apiKey: process.env.ALGOLIA_API_KEY,
        indexName: 'physical-ai-humanoid-robotics',
      }
    }),

  // Custom fields for textbook functionality
  customFields: {
    textbookVersion: '1.0.0',
    lastUpdated: new Date().toISOString(),
    chatbotEnabled: true,
    chatbotEndpoint: process.env.CHATBOT_API_URL || 'http://localhost:8000',
  },

  // Plugins for enhanced functionality
  plugins: [
    // Plugin for AI chat widget
    [
      './src/plugins/docusaurus-plugin-ai-chat',
      {
        backendUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000',
      },
    ],
    // Plugin for educational features
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            to: '/docs/chapter-1-introduction-to-physical-ai',
            from: ['/docs', '/textbook', '/introduction'],
          },
        ],
      },
    ],
  ],
};

export default config;