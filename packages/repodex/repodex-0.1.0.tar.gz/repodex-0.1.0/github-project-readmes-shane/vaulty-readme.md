# Vaulty

A VSCode extension for managing API keys using your system's secure keychain.

## Important Security Notes

- This extension handles sensitive data. While we use your system's secure keychain, no security measure is perfect.
- The extension's security depends on your system's security. A compromised system means compromised keys.
- VSCode extensions run with your user privileges. Review the code before trusting with sensitive keys.
- While metadata (key names, categories) syncs with VSCode settings, actual key values never leave your system.
- Consider your threat model: this extension may not be suitable for high-security environments.

## Core Functionality

### Storage

- Uses system keychain:
  - Windows: Credential Manager
  - macOS: Keychain Access
  - Linux: libsecret
- Stores only metadata (names, categories) in VSCode storage
- No plain text storage of sensitive values
- Local-only, no cloud sync

### Organization

- Category-based key management
- Drag-and-drop reordering of:
  - Keys within categories
  - Categories themselves
- Real-time search filtering
- Collapsible category sections

### Commands

```txt
vaulty.storeKey  - Store a new API key
vaulty.getKey    - Copy a key to clipboard
vaulty.listKeys  - View and manage stored keys
```

### UI Integration

- Native VSCode webview implementation
- Uses VSCode's theming system
- Command palette integration
- Password-protected input fields

## Technical Implementation

### Security

- VSCode SecretStorage API for secure key storage
- Encrypted at rest via system keychain
- Memory sanitization (clearing sensitive fields)
- No network operations

### Data Structure

- Keys: `{ name: string, category?: string }`
- Categories: `{ name: string, expanded: boolean, order: number }`
- Metadata stored in VSCode's globalState
- Values stored in system keychain

### State Management

- Real-time UI updates
- Persistent category state
- Error handling with user feedback
- Automatic cleanup on deactivation

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions.

## Security Verification

See [SECURITY_VERIFICATION.md](SECURITY_VERIFICATION.md) for steps to verify security claims.

## Limitations

- No built-in key rotation or expiration management
- No audit logging of key access
- No team sharing features
- No backup/restore functionality
- Limited to VSCode's extension security model

## License

MIT - However, use at your own risk. No warranty for security or fitness for a particular purpose.
