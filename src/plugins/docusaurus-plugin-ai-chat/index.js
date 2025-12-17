const path = require('path');

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-ai-chat',

    getClientModules() {
      return [path.resolve(__dirname, './client.js')];
    },

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@chat-widget': path.resolve(__dirname, '../components/ChatWidget'),
          },
        },
      };
    },

    injectHtmlTags() {
      return {
        postBodyTags: [
          `<div id="ai-chat-root"></div>`,
        ],
      };
    },
  };
};