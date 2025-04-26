# Image Name Processor

A Python application that automatically generates descriptive filenames for images using AI. It can watch directories for new images and rename them based on their content using the Ollama LLaVA model.

## Features

- 🤖 AI-powered descriptive filename generation using LLaVA model
- 👀 Directory watching for automatic processing of new images
- 🖼️ Supports multiple image formats (PNG, JPG, JPEG)
- 🔒 Safe file operations with retry mechanisms
- ✅ Image verification before processing
- 🧹 Clean filename generation (alphanumeric with hyphens)
- 📝 Detailed logging for monitoring and debugging
- 🔄 Memory management with garbage collection

## Prerequisites

- Python 3.x
- [Ollama](https://ollama.ai/) installed and running
- LLaVA model (`ollama pull llava:13b`)

## Quick Start

1. Create and activate virtual environment:

    ```bash
    python -m venv venv
    # Activate based on your OS:
    # Windows: .\venv\Scripts\activate
    # Unix: source venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    # Watch a directory
    python main.py /path/to/directory

    # Process a single file
    python main.py /path/to/image.jpg
    ```

## Usage Examples

### Watch Directory Mode

Run the script to monitor a directory for new images:

```bash
# Watch Desktop for new images
python main.py ~/Desktop

# Watch Downloads folder
python main.py ~/Downloads
```

The script will:

- Monitor the specified directory for new image files
- Automatically process and rename new images as they appear
- Continue running until interrupted (Ctrl+C)

### Single File Mode

Process a specific image file:

```bash
python main.py path/to/image.jpg
```

The script will:

- Verify the image file
- Generate a descriptive name using AI
- Safely rename the file
- Exit after processing

## Technical Details

### Safety Features

1. **File Verification**:
   - Validates image files before processing
   - Ensures files are completely written before renaming
   - Uses PIL for image integrity checks

2. **Safe File Operations**:
   - Copy-then-delete strategy for safe moves
   - Multiple retry attempts for file operations
   - Garbage collection to prevent file handle issues
   - Delay mechanisms to ensure file system stability

3. **Error Handling**:
   - Comprehensive logging of all operations
   - Graceful failure handling
   - Detailed error messages for debugging

### AI Integration

- Uses Ollama's LLaVA model for image analysis
- Generates concise 4-5 word descriptions
- Converts descriptions to clean filenames:
  - Lowercase conversion
  - Special character removal
  - Space replacement with hyphens

### Memory Management

- Active garbage collection after file operations
- Handle cleanup after image processing
- Resource management for long-running operations

## Example Transformations

Original filenames → AI-generated names:

- `IMG_20231220_193001.jpg` → `a-rocket-launch.jpg`
- `Screenshot_2023.png` → `girl-eating-donut-smiling.png`
- `DSC_0123.jpg` → `man-smoking-cigarette-and-wearing-suit.jpg`

## Troubleshooting

1. **File Access Issues**:
   - Ensure proper permissions on directories
   - Check for file locks from other applications
   - Verify sufficient disk space

2. **AI Service Issues**:
   - Confirm Ollama is running (`http://localhost:11434`)
   - Verify LLaVA model is installed
   - Check network connectivity

3. **Memory Issues**:
   - Monitor system resources during operation
   - Consider processing fewer files simultaneously
   - Ensure adequate system memory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Ollama](https://ollama.ai/) and the LLaVA model
- Uses [Watchdog](https://pythonhosted.org/watchdog/) for file system monitoring
- Inspired by the need for automated, intelligent file organization
