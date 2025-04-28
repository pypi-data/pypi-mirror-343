# markdown2app
markdown2app.plainmark.com

# Plainmark

Plainmark is a lightweight programming language embedded in Markdown that runs across multiple platforms including web browsers, terminal environments, desktop applications, and mobile devices.

## What is Plainmark?

Plainmark allows you to write both documentation and executable code in the same Markdown file. Code blocks tagged with ```plainmark are interpreted and executed by the Plainmark runtime.

## Key Features

- **Write Once, Run Anywhere**: The same Plainmark code works across all supported platforms
- **Embedded in Markdown**: Combine documentation and executable code in a single file
- **Platform-Specific APIs**: Access platform capabilities like file system, device sensors, etc.
- **Interactive Documents**: Create dynamic, interactive documentation
- **Easy to Learn**: Familiar JavaScript-like syntax

## Platform Implementation Guide

### Browser Implementation

The browser implementation uses JavaScript to interpret and execute Plainmark code. It consists of:

1. An HTML file that provides the editor interface
2. A JavaScript interpreter that extracts code blocks and executes them
3. DOM manipulation capabilities for UI rendering

**Running in Browser:**
1. Open `index.html` in any modern browser
2. Write your Plainmark code in the editor
3. Click "Run" to execute

### Terminal/Python Implementation

The Python implementation allows running Plainmark in any terminal environment. It consists of:

1. A Python script (`plainmark.py`) that processes Markdown files
2. A code extractor and interpreter for Plainmark code blocks
3. Python-based API for file system access and terminal commands

**Running in Terminal:**
```bash
# Execute a file
python plainmark.py example.md

# Start REPL mode
python plainmark.py --repl

# Create an example file
python plainmark.py --example
```

### Desktop Implementation (Electron)

The desktop implementation provides a native application experience using Electron. It consists of:

1. A main process (`main.js`) that handles application lifecycle
2. A renderer process (`index.html`) with the editor UI
3. IPC communication for file operations
4. Full system access through Node.js APIs

**Building for Desktop:**
```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Build for distribution
npm run build
```

### Mobile Implementation (Android)

The Android implementation runs Plainmark on mobile devices. It consists of:

1. A Kotlin-based Android app
2. A WebView for executing Plainmark code
3. JavaScript interfaces for accessing device features (camera, sensors, etc.)
4. Integration with the Android filesystem

**Building for Android:**
1. Open the project in Android Studio
2. Connect an Android device or start an emulator
3. Build and run the app

## Plainmark Syntax Examples

### Basic Syntax

```markdown
# My Plainmark Program

This is a simple program.

```plainmark
// Variables
let name = "World";
let number = 42;

// Output
print("Hello, " + name + "!");
print("The answer is: " + number);
```
```

### Platform-Specific Features

```markdown
# Cross-Platform Example

```plainmark
// Detect platform
let platform;
if (typeof window !== 'undefined' && window.Android) {
  platform = "Android";
} else if (typeof process !== 'undefined' && process.versions.electron) {
  platform = "Desktop";
} else if (typeof document !== 'undefined') {
  platform = "Browser";
} else {
  platform = "Terminal";
}

print("Running on: " + platform);

// Use platform-specific features
if (platform === "Android") {
  // Mobile-specific code
  let acceleration = JSON.parse(readSensor("accelerometer"));
  print("Device acceleration: " + acceleration.x + ", " + acceleration.y + ", " + acceleration.z);
} else if (platform === "Desktop") {
  // Desktop-specific code
  let sysInfo = getSystemInfo();
  print("CPU cores: " + sysInfo.cpus);
} else if (platform === "Browser") {
  // Browser-specific code
  document.body.innerHTML += "<div>Running in browser!</div>";
} else {
  // Terminal-specific code
  print("Current directory: " + executeCommand("pwd"));
}
```
```

## Use Cases

- **Educational tools** - Interactive learning materials and tutorials
- **Documentation** - Self-executing technical documentation
- **Prototyping** - Quick application development across platforms
- **Note-taking** - Executable notes and code snippets
- **Data analysis** - Process and visualize data in Markdown

## License

