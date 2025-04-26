# Airport - for .air files

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Airport is a VSCode extension that introduces `.air` as the universal configuration format for AI coding assistants, while maintaining seamless compatibility with platform-specific formats like `.github/copilot-instructions.md`, `.clinerules`, and `.cursorrules`.

## Why Airport?

Just as `.editorconfig` standardized editor settings and `.prettierrc` unified code formatting, `.air` aims to become the universal configuration format for AI coding assistants. Airport automatically synchronizes your `.air` rules to all platform-specific formats, ensuring compatibility while pushing towards standardization.

## Features

- Central sync source of truth
- Real-time synchronization to vendor formats
- Support for vendor-specific capabilities
- Easy configuration and management
- Status monitoring and validation

## Installation

```bash
# Via VSCode Marketplace
ext install airport

# Or from VSIX
code --install-extension airport-x.x.x.vsix
```

## Quick Start

1. Create an `.air` file in your project root
2. Define your AI assistant rules
3. Airport automatically syncs to platform-specific formats

Example `.air` file:

```markdown
## Core Rules
- Follow project style guide
- Write tests for new features
- Document public APIs

## Vendor Extensions
@copilot {
  use_completion_context: true
  suggest_tests: true
}

@cursor {
  use_function_extraction: true
  analyze_imports: deep
}
```

## Commands

- `Airport: Add Custom Vendor`: Add a new custom vendor configuration
- `Airport: Configure Vendors`: Configure vendor-specific settings
- `Airport: Sync Rules`: Manually sync rules across vendors
- `Airport: Show Status`: Display current sync status
- `Airport: Open Configuration`: Open Airport configuration
- `Airport: Enable/Disable Sync`: Toggle sync functionality
- `Airport: Validate Rules`: Validate rule files

TODO document command for custom vendor

## Configuration

Configure Airport through VSCode settings:

```jsonc
{
  "airport.enabled": true,
  "airport.source": ".air",
  "airport.defaultFormat": "markdown",
  // See full configuration options in documentation
}
```

## Development

### Prerequisites

- Node.js (Latest LTS)
- VSCode (Latest Stable)
- TypeScript (Latest Stable)
- Git (Latest)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/airport.git
cd airport

# Install dependencies
npm install

# Setup git hooks
npm run prepare
```

### Development Workflow

1. Create feature branch
2. Write tests (TDD approach)
3. Implement feature
4. Run full test suite
5. Submit pull request

For detailed development guidelines, see [Development Guide](dev/development-guide.md).

## Documentation

- [Core Concept](dev/airport-concept.md)
- [Development Guide](dev/development-guide.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- File bugs/issues in our [Issue Tracker](https://github.com/yourusername/airport/issues)
- Read our [documentation](dev/) for detailed guides
- Join our [community discussions](https://github.com/yourusername/airport/discussions)

## Acknowledgments

Special thanks to all contributors who help make Airport better!
