import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/airas/ja/blog',
    component: ComponentCreator('/airas/ja/blog', '8e9'),
    exact: true
  },
  {
    path: '/airas/ja/blog/archive',
    component: ComponentCreator('/airas/ja/blog/archive', '862'),
    exact: true
  },
  {
    path: '/airas/ja/blog/sample',
    component: ComponentCreator('/airas/ja/blog/sample', 'a17'),
    exact: true
  },
  {
    path: '/airas/ja/markdown-page',
    component: ComponentCreator('/airas/ja/markdown-page', 'd26'),
    exact: true
  },
  {
    path: '/airas/ja/docs',
    component: ComponentCreator('/airas/ja/docs', 'e44'),
    routes: [
      {
        path: '/airas/ja/docs',
        component: ComponentCreator('/airas/ja/docs', '14f'),
        routes: [
          {
            path: '/airas/ja/docs',
            component: ComponentCreator('/airas/ja/docs', 'ac2'),
            routes: [
              {
                path: '/airas/ja/docs/component/analytic-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/analytic-subgraph', 'cbd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/executor',
                component: ComponentCreator('/airas/ja/docs/component/executor', '7ba'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/experimental-plan-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/experimental-plan-subgraph', '09f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/generator',
                component: ComponentCreator('/airas/ja/docs/component/generator', '046'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/html-uploader',
                component: ComponentCreator('/airas/ja/docs/component/html-uploader', 'b96'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/latex-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/latex-subgraph', '33c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/readme-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/readme-subgraph', '9ab'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/research-preparation-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/research-preparation-subgraph', '6e5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/retrieve-paper-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/retrieve-paper-subgraph', '215'),
                exact: true
              },
              {
                path: '/airas/ja/docs/component/review-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/review-subgraph', '8fc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/component/writer-subgraph',
                component: ComponentCreator('/airas/ja/docs/component/writer-subgraph', '060'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/development/local-setup',
                component: ComponentCreator('/airas/ja/docs/development/local-setup', '031'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/development/MCP',
                component: ComponentCreator('/airas/ja/docs/development/MCP', 'c1c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/development/roadmap',
                component: ComponentCreator('/airas/ja/docs/development/roadmap', '0e1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/intro',
                component: ComponentCreator('/airas/ja/docs/intro', 'fa1'),
                exact: true
              },
              {
                path: '/airas/ja/docs/introduction',
                component: ComponentCreator('/airas/ja/docs/introduction', 'd31'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/quickstart',
                component: ComponentCreator('/airas/ja/docs/quickstart', 'd61'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/airas/ja/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/congratulations', '6ab'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/create-a-blog-post', '807'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/create-a-document', 'a1c'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/create-a-page', '7ef'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/deploy-your-site', 'd04'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/airas/ja/docs/tutorial-basics/markdown-features', '539'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/airas/ja/docs/tutorial-extras/manage-docs-versions', '71b'),
                exact: true
              },
              {
                path: '/airas/ja/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/airas/ja/docs/tutorial-extras/translate-your-site', '26c'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/airas/ja/',
    component: ComponentCreator('/airas/ja/', 'fe1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
