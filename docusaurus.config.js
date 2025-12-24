// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'A Comprehensive Guide to Embodied Intelligence',
  favicon: 'img/favicon.ico',

  url: 'https://shabnamwahid.github.io',
 
  baseUrl: '/physical-ai-humanoid-robotics-book-final/',

  organizationName: 'Shabnamwahid',
  projectName: 'physical-ai-humanoid-robotics-book-final',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  // onBrokenMarkdownLinks: 'warn',
  onBrokenMarkdownLinks: 'throw', 
  
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
      },
      ur: {
        direction: 'rtl',
        label: 'اردو',
      },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'), 
          editUrl:
            'https://github.com/Shabnamwahid/physical-ai-humanoid-robotics-book-final/tree/main/',
        },
        blog: false,
        theme: {
           customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            to: '/chapter-1-introduction-to-physical-ai',  // direct Chapter 1 pe jaaye
            position: 'left',
            label: 'Textbook',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            href: 'https://github.com/Shabnamwahid/physical-ai-humanoid-robotics-book-final/issues',
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
                to: '/chapter-1-introduction-to-physical-ai',
              },
              {
                label: 'Humanoid Robotics Basics',
                to: '/chapter-2-basics-of-humanoid-robotics',
              },
              {
                label: 'ROS 2 Fundamentals',
                to: '/chapter-3-ros-2-fundamentals',
              },
              {
                label: 'Digital Twin Simulation',
                to: '/chapter-4-digital-twin-simulation',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Shabnamwahid/physical-ai-humanoid-robotics-book-final/issues',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Report Issues',
                href: 'https://github.com/Shabnamwahid/physical-ai-humanoid-robotics-book-final/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'json', 'yaml'],
      },
    }),

  customFields: {
    textbookVersion: '1.0.0',
    lastUpdated: new Date().toISOString(),
    chatbotEnabled: true,
    chatbotEndpoint: process.env.CHATBOT_API_URL || 'http://localhost:8000',
  },

  plugins: [
    // [
    //   './src/plugins/docusaurus-plugin-ai-chat',
    //   {
    //     backendUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000',
    //   },
    // ],
    // [
    //   '@docusaurus/plugin-client-redirects',
    //   {
    //     redirects: [
    //       {
    //         to: '/docs/chapter-1-introduction-to-physical-ai',
    //         from: ['/docs', '/textbook', '/introduction'],
    //       },
    //     ],
    //   },
    // ],
  ],
};

export default config;