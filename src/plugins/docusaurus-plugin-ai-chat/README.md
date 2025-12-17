# Docusaurus AI Chat Plugin

This plugin adds an AI chat widget to your Docusaurus site, allowing users to ask questions about your content and get AI-powered responses.

## Features

- Floating chat widget that appears on all pages
- Context-aware responses based on your documentation
- Conversation history
- Source attribution
- Confidence scoring
- Dark/light mode support
- Mobile-responsive design

## Installation

1. Place this plugin in your `src/plugins/docusaurus-plugin-ai-chat` directory
2. Add the plugin to your Docusaurus config:

```js
// docusaurus.config.js
module.exports = {
  // ... other config
  plugins: [
    // ... other plugins
    [
      './src/plugins/docusaurus-plugin-ai-chat',
      {
        backendUrl: 'https://your-backend-url.com', // Optional, defaults to http://localhost:8000
      },
    ],
  ],
};
```

## Configuration

### Plugin Options

- `backendUrl` (optional): The URL of your AI backend service. Defaults to `http://localhost:8000`.

### Runtime Configuration

You can also configure the backend URL at runtime by setting a global variable:

```html
<script>
  window.chatConfig = {
    backendUrl: 'https://your-backend-url.com'
  };
</script>
```

## Usage

Once installed, the chat widget will appear as a floating button on the bottom right of your pages. Users can click it to open the chat interface and ask questions about your content.

## How It Works

The plugin integrates with your AI backend service to provide context-aware responses. When a user asks a question:

1. The question is sent to your backend service
2. The backend retrieves relevant content from your documentation
3. An AI model generates a response based on the retrieved content
4. The response is displayed in the chat widget with source attribution

## Customization

### Styling

The chat widget can be customized by modifying the CSS in the component. The component uses CSS variables that adapt to Docusaurus's theme system.

### Positioning

The widget is positioned at the bottom right by default. You can adjust this by modifying the CSS positioning rules.

## API Integration

The plugin expects your backend to provide the following endpoints:

- `POST /api/v1/chat`: Main chat endpoint
  - Request: `{ message: string, conversation_id?: string }`
  - Response: `{ response: string, conversation_id: string, sources?: string[], confidence?: number }`

Make sure your backend service is running and accessible from your Docusaurus site.

## Development

To modify the chat widget:

1. Update the React component in `src/components/ChatWidget/ChatWidget.jsx`
2. Update styles in `src/components/ChatWidget/ChatWidget.css`
3. Test locally with `npm run start`

## Troubleshooting

### Widget Not Appearing

- Make sure the plugin is properly added to your Docusaurus config
- Check browser console for JavaScript errors
- Verify that React and ReactDOM are properly loaded

### Backend Connection Issues

- Verify that your backend service is running
- Check that the backend URL is correct
- Ensure CORS is properly configured on your backend

### Styling Issues

- Make sure the CSS file is properly loaded
- Check for CSS conflicts with your site's existing styles
- Verify that the component is compatible with your Docusaurus version