# `warpdeck-chat`

warpdeck mkdocs chat app

Embedded MkDocs AI Chat Assistant called `warpdeck` - Project Brief

## Open Dev Environment

I'm not including the env build setup here. Initialized with:

```sh
conda deactivate
.venv\Scripts\activate
```

```sh
mkdocs build # or mkdocs serve
```

> [!NOTE]
> If you get this error: `Failed to canonicalize script path` I can guarantee you renamed your renamed project dir AFTER building the env with `uv venv` ! ... and good luck finding that solve in google or ai! I had to delete the venv and start again. I'm not sure if this is a bug or a feature, but it's a pain.

## Overview

We need a JavaScript chat widget that can be embedded in MkDocs sites to provide contextual help using AI. The widget should integrate seamlessly with MkDocs Material theme and provide a smooth user experience without disrupting the existing documentation flow.

> [!TIP]
> All classes will be prefixed with `warpdeck-` to avoid conflicts with existing styles and functions, unless of course we decide to use the Material theme classes. See below for that.

---

> [!IMPORTANT]
> NEVER Write a single line of code before backing up that file via commandline first!
> Critical all code is kept modular with very concise comments so when we need to query Ai, the context sent doesn't blow out the API calls. This is a critical development requirement as we are not JS experts. Hand holding is needed here.
>
> Backup all files via commandline before implementing changes, then test changes before writing new code. If changes succeed and you and Ai are happy, then commit changes to git with minimal chore: comments - rinse and repeat! Both you and Ai must follow these instructions to the letter.

## Core Components

### 1. Chat Button

- [x] Floating action button (FAB) positioned in bottom-right corner
- [x] Material Design style with a a custom Anthropic Logo chat/message icon
- [x] Smooth hover and click animations
- [ ] Adapts to MkDocs Material theme colors - this is somewhat working, but needs to be more robust

### 2. Chat Modal

- [x] Uses fontawesome icons for chat and close buttons etc, currently svgs are hardcoded in js . Not good, so solve this first!
- [x] Clean, minimal interface similar to modern chat applications
- [x] Header with title and close button
- [x] Message container for chat history
- [x] Input area with text field and send button
- [x] Loading states and animations and messages
- [ ] Dark/light theme support matching MkDocs
- [ ] Dynamically adjust the placeholder text to match and be title / tag aware of the current page

For both:

- [ ] Further modularize the JS code, specifically the `embed.js` file. Important!
- [ ] Change these to better match the theme classes

```css
.warpdeck-message {
  font-size: .8rem;
}

warpdeck-modal-content {
  max-width: 800px;
}
```

- [ ] Add Mock Username and Avatar to messages
- [ ] Add Mock Assistant name and Avatar to messages
- [x] Add a loading spinner to the message waiting for the response
- [ ] Add smooth message transitions - maybe use a library for some of these or try a leverage the site theme libraries
- [ ] Change ask me anything about this documentation to be more specific to the current page and also .8rem font size
- [ ] code highlighting for the messages
- [ ] Expand the oneliner message input field to a deeper field with a button to expand from the oneliner
- [ ] Need to be able to shift enter for a new line in the message input field
- [ ] Add a copy to clipboard button to the to any message field

### 3. Context Management

- [ ] Extract content from current documentation page possibly by default
    - [ ] button to send current page content to the AI
    - [ ] or ask a non related page question to the AI
    - [ ] System-Prompts to handle these sends will be sidecars files, won't placed in javascript code. Makes for much easier updates.
- [ ] Clean and format content for AI context
    - [ ] or even better reach into the mkdocs dir to grab the corresponding markdown file!
- [x] Handle page navigation and context updates
- [ ] Button option to allow user to send new context of append context to the current context
- [ ] Button to all clear all past context - currently stored in local storage
- [ ] Regex to watch for secrets patterns and not send them to the AI, use: [secrets-regex](.resources/scripts/scan_secrets.py) flash modal if attempted

### 4. Mock API Integration (Initial Phase)

- [ ] Simulated responses for development. I have a basic singular mock response working already. Need more.
- [ ] Randomized response delays
- [ ] Context-aware mock responses, randomized responses
- [ ] Error state handling, like in Anthropic Claude is offline or a secret  was detected

## Technical Requirements

### File Structure

```tree
docs/
├── javascripts/
│   ├── embed.js            # Main implementation
│   ├── loader.js           # Script loader
│   └── warpdeck-config.js  # Configuration
```

### Configuration Integration

Added to mkdocs.yml:

```yaml
extra_javascript:
  - javascripts/warpdeck-config.js
  - javascripts/loader.js
```

#### Base Configuration

```javascript
window.WarpDeckConfig = {
  debug: true,
  position: 'bottom-right',
  theme: 'auto',
  mockDelay: 1000,
  primaryColor: '#000000'
};
```

## Implementation Details

### React Demo Implementation

For reference, here's how the UI components should look and behave (in React):

```typescript
import React, { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';

const MkDocsAIDemo = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const mockResponse = async (question) => {
    setIsLoading(true);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const response = `This is a simulated response to your question: "${question}". In a real implementation, this would come from the Anthropic Claude API using the current page's context.`;

    setMessages(prev => [...prev,
      { type: 'user', content: question },
      { type: 'assistant', content: response }
    ]);
    setIsLoading(false);
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const question = input.trim();
    setInput('');
    await mockResponse(question);
  };

  return (
    <div className="font-sans">
      {/* Floating Action Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-lg hover:bg-blue-700 transition-colors"
        aria-label="WarpDeck AI Assistant"
      >
        <MessageCircle size={24} />
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg w-full max-w-2xl h-[600px] flex flex-col shadow-xl">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b">
              <h3 className="text-lg font-semibold">Documentation Assistant</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-500 hover:text-gray-700"
                aria-label="Close"
              >
                <X size={24} />
              </button>
            </div>

            {/* Chat Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg ${
                    msg.type === 'user'
                      ? 'bg-blue-100 ml-12'
                      : 'bg-gray-100 mr-12'
                  }`}
                >
                  {msg.content}
                </div>
              ))}
              {messages.length === 0 && (
                <div className="text-center text-gray-500 mt-8">
                  Ask any question about the documentation!
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="p-4 border-t">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask a question about this page..."
                  className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSend}
                  disabled={isLoading}
                  className={`px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center space-x-2 ${
                    isLoading
                      ? 'opacity-50 cursor-not-allowed'
                      : 'hover:bg-blue-700'
                  }`}
                >
                  {isLoading ? (
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <Send size={20} />
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MkDocsAIDemo;
```

## Key Features

### Theme Integration

- Match MkDocs Material color scheme
- Support dark/light mode switching
- Use CSS variables for theme colors
- Responsive design for mobile/desktop

### Accessibility

- Proper ARIA labels
- Keyboard navigation
- Focus management
- High contrast support

### User Experience

- Smooth animations
- Clear loading states
- Error handling
- Empty state messages
- Message history scrolling
- Input focus management

### Development Features

- Debug mode with console logging
- Mock API responses
- Configurable delays
- Error simulation

## Implementation Guidelines

1. Load order is critical:
   - Config must load first
   - Loader manages embed.js injection
   - Initialization after DOM ready with 3 sec delay

2. Escape sequences:
   - Avoid unnecessary string escaping in SVGs
   - Use template literals for HTML templates

3. Event handling:
   - Proper cleanup of event listeners
   - Handle modal closing cases
   - Keyboard interaction support

4. Style injection:
   - Use unique class names (although Im considering the use of Tailwind CSS or simply use the class names from the Material theme)
   - CSS variable fallbacks
   - Mobile-first responsive design

## Error Handling

1. Configuration:
   - Validate required config
   - Provide sensible defaults
   - Log helpful error messages

2. Runtime:
   - Graceful fallbacks
   - User-friendly error messages
   - Debug logging in development

3. API:
   - Timeout handling
   - Retry logic
   - Error state UI

## Development Setup

1. Clone MkDocs site
2. Add configuration to mkdocs.yml
3. Create javascripts directory
4. Add implementation files
5. Run MkDocs server
6. Test in different themes/modes

## Testing Checklist

1. Basic Functionality
   - [x] Button renders correctly (fontawesome), there is a bug in certain pages where the chat button is malformed. See below
   - [x] Modal opens/closes
   - [x] Messages display properly
   - [x] Input handling works

2. Theme Support
   - [ ] Light mode styling
   - [ ] Dark mode styling
   - [ ] Color scheme switching

3. Responsive Design
   - [x] Mobile layout
   - [x] Desktop layout
   - [x] Different screen sizes

4. Error States
   - [ ] Configuration errors
   - [ ] Network errors
   - [ ] Input validation

## Next Steps

1. Phase 1: MVP
   - [x] Basic UI implementation
   - [x] Mock API integration via a fake response
   - [ ] Theme support is somewhat working, but needs to be more robust
   - [ ] Error handling

2. Phase 2: API Integration
   - [ ] Real API endpoints
   - [ ] Authentication
   - [ ] Rate limiting
   - [ ] Response streaming

3. Phase 3: Enhancement
   - [ ] Caching
   - [ ] Analytics
   - [ ] Custom styling
   - [ ] Additional features
   - [ ] SSO integration so chats can be saved and continued across sessions

## Current Bugs

- [ ] none
