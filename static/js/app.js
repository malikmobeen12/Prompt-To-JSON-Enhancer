/**
 * Prompt-to-JSON Enhancer Frontend JavaScript
 * Handles user interactions, API calls, and UI updates
 */

class PromptEnhancer {
  constructor() {
    this.initializeElements();
    this.bindEvents();
  }

  initializeElements() {
    this.promptInput = document.getElementById("prompt-input");
    this.transformBtn = document.getElementById("transform-btn");
    this.outputSection = document.getElementById("output-section");
    this.jsonOutput = document.getElementById("json-output");
    this.loading = document.getElementById("loading");
    this.error = document.getElementById("error");
    this.errorText = document.getElementById("error-text");
    this.copyBtn = document.getElementById("copy-btn");
    this.downloadBtn = document.getElementById("download-btn");
    this.toast = document.getElementById("toast");
    this.themeToggle = document.getElementById("theme-toggle");
    this.themeIcon = this.themeToggle?.querySelector(".theme-icon");

    // New floating panel elements
    this.fabSettings = document.getElementById("fab-settings");
    this.floatingPanel = document.getElementById("floating-panel");
    this.panelOverlay = document.getElementById("panel-overlay");
    this.panelClose = document.getElementById("panel-close");
    this.styleButtons = document.querySelectorAll(".style-btn");
    this.includeKeysCheckboxes = document.querySelectorAll(
      'input[name="include-keys"]'
    );

    // Initialize current settings
    this.currentOutputStyle = "detailed";
  }

  bindEvents() {
    this.transformBtn.addEventListener("click", () => this.transformPrompt());
    this.copyBtn.addEventListener("click", () => this.copyToClipboard());
    this.downloadBtn.addEventListener("click", () => this.downloadJSON());

    // Theme toggle functionality
    if (this.themeToggle) {
      this.themeToggle.addEventListener("click", () => this.toggleTheme());
    }

    // Floating panel functionality
    if (this.fabSettings) {
      this.fabSettings.addEventListener("click", () =>
        this.showFloatingPanel()
      );
    }

    if (this.panelClose) {
      this.panelClose.addEventListener("click", () => this.hideFloatingPanel());
    }

    if (this.panelOverlay) {
      this.panelOverlay.addEventListener("click", () =>
        this.hideFloatingPanel()
      );
    }

    // Style toggle buttons
    this.styleButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => this.handleStyleToggle(e));
    });

    // Allow Enter key to trigger transformation (Ctrl+Enter or Cmd+Enter)
    this.promptInput.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        this.transformPrompt();
      }
    });

    // Auto-resize textarea
    this.promptInput.addEventListener("input", () => {
      this.promptInput.style.height = "auto";
      this.promptInput.style.height = this.promptInput.scrollHeight + "px";
    });

    // Close panel on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.floatingPanel.classList.contains("show")) {
        this.hideFloatingPanel();
      }
    });
  }

  async transformPrompt() {
    const prompt = this.promptInput.value.trim();

    if (!prompt) {
      this.showError("Please enter a prompt to transform.");
      return;
    }

    this.showLoading();
    this.hideError();
    this.hideOutput();

    try {
      // Check if customization options are being used
      const hasCustomOptions = this.hasCustomSettings();
      const endpoint = hasCustomOptions ? "/transform/custom" : "/transform";

      const requestBody = { prompt };

      if (hasCustomOptions) {
        const includeKeys = Array.from(this.includeKeysCheckboxes)
          .filter((checkbox) => checkbox.checked)
          .map((checkbox) => checkbox.value);

        requestBody.include_keys = includeKeys;
        requestBody.output_style = this.currentOutputStyle;
      }

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to transform prompt");
      }

      this.displayResult(data);
    } catch (error) {
      console.error("Error transforming prompt:", error);
      this.showError(
        error.message || "An unexpected error occurred. Please try again."
      );
    } finally {
      this.hideLoading();
    }
  }

  displayResult(data) {
    // Format JSON with proper indentation
    const formattedJson = JSON.stringify(data, null, 2);

    // Update the code element content
    const codeElement = this.jsonOutput.querySelector("code");
    codeElement.textContent = formattedJson;

    // Highlight syntax using Prism.js
    if (window.Prism) {
      Prism.highlightElement(codeElement);
    }

    // Show output section with animation
    this.outputSection.style.display = "block";
    this.outputSection.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }

  async copyToClipboard() {
    const codeElement = this.jsonOutput.querySelector("code");
    const text = codeElement.textContent;

    try {
      await navigator.clipboard.writeText(text);
      this.showToast();
      this.updateCopyButton();
    } catch (error) {
      console.error("Failed to copy to clipboard:", error);
      // Fallback for older browsers
      this.fallbackCopyToClipboard(text);
    }
  }

  fallbackCopyToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      this.showToast();
      this.updateCopyButton();
    } catch (error) {
      console.error("Fallback copy failed:", error);
    }

    document.body.removeChild(textArea);
  }

  updateCopyButton() {
    const copyIcon = this.copyBtn.querySelector(".copy-icon");
    const copyText = this.copyBtn.querySelector(".copy-text");

    this.copyBtn.classList.add("copied");
    copyIcon.textContent = "✓";
    copyText.textContent = "Copied!";

    setTimeout(() => {
      this.copyBtn.classList.remove("copied");
      copyIcon.textContent = "📋";
      copyText.textContent = "Copy";
    }, 2000);
  }

  showToast() {
    this.toast.classList.add("show");
    setTimeout(() => {
      this.toast.classList.remove("show");
    }, 3000);
  }

  showLoading() {
    this.loading.style.display = "block";
    this.transformBtn.disabled = true;
    this.transformBtn.querySelector(".btn-text").textContent =
      "Transforming...";
  }

  hideLoading() {
    this.loading.style.display = "none";
    this.transformBtn.disabled = false;
    this.transformBtn.querySelector(".btn-text").textContent =
      "Transform to JSON";
  }

  showError(message) {
    this.errorText.textContent = message;
    this.error.style.display = "flex";
    this.error.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }

  hideError() {
    this.error.style.display = "none";
  }

  hideOutput() {
    this.outputSection.style.display = "none";
  }

  // Theme management methods
  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    this.setTheme(newTheme);
    this.updateThemeIcon(newTheme);
    this.saveThemePreference(newTheme);
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }

  updateThemeIcon(theme) {
    if (this.themeIcon) {
      this.themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
    }
  }

  saveThemePreference(theme) {
    localStorage.setItem("theme", theme);
  }

  loadThemePreference() {
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const theme = savedTheme || (prefersDark ? "dark" : "light");

    this.setTheme(theme);
    this.updateThemeIcon(theme);
  }

  // Floating panel methods
  showFloatingPanel() {
    this.floatingPanel.classList.add("show");
    this.panelOverlay.classList.add("show");
    document.body.style.overflow = "hidden";
  }

  hideFloatingPanel() {
    this.floatingPanel.classList.remove("show");
    this.panelOverlay.classList.remove("show");
    document.body.style.overflow = "";
  }

  handleStyleToggle(e) {
    const clickedBtn = e.target;
    const style = clickedBtn.getAttribute("data-style");

    // Update active button
    this.styleButtons.forEach((btn) => btn.classList.remove("active"));
    clickedBtn.classList.add("active");

    // Update current style
    this.currentOutputStyle = style;
  }

  hasCustomSettings() {
    // Check if any settings are different from defaults
    const hasCustomStyle = this.currentOutputStyle !== "detailed";
    const hasCustomKeys = Array.from(this.includeKeysCheckboxes).some(
      (checkbox) => !checkbox.checked
    );

    return hasCustomStyle || hasCustomKeys;
  }

  // Download functionality
  downloadJSON() {
    const codeElement = this.jsonOutput.querySelector("code");
    const jsonText = codeElement.textContent;

    if (!jsonText) {
      this.showError("No JSON data to download");
      return;
    }

    try {
      const blob = new Blob([jsonText], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `prompt-transformation-${new Date()
        .toISOString()
        .slice(0, 19)
        .replace(/:/g, "-")}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      this.showToast("JSON file downloaded successfully!");
    } catch (error) {
      console.error("Download failed:", error);
      this.showError("Failed to download JSON file");
    }
  }
}

// Initialize the application when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  const app = new PromptEnhancer();
  app.loadThemePreference();
});

// Add some example prompts for better UX
const examplePrompts = [
  "Write a Python function to scrape a website and save results to CSV",
  "Create a SQL query to find the top 10 customers by revenue",
  "Build a JavaScript function to validate email addresses",
  "Explain how Docker containers work",
  "Create a React component for a todo list",
];

// Add example prompt suggestions (optional enhancement)
function addExamplePrompts() {
  const promptInput = document.getElementById("prompt-input");

  // Add click handler to load examples
  const examplesContainer = document.createElement("div");
  examplesContainer.className = "examples-container";
  examplesContainer.innerHTML = `
        <p class="examples-label">Try these examples:</p>
        <div class="examples-list">
            ${examplePrompts
              .map(
                (prompt) =>
                  `<button class="example-btn" data-prompt="${prompt.replace(
                    /"/g,
                    "&quot;"
                  )}">${prompt}</button>`
              )
              .join("")}
        </div>
    `;

  promptInput.parentNode.insertBefore(
    examplesContainer,
    promptInput.nextSibling
  );

  // Add event listeners to example buttons
  examplesContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("example-btn")) {
      const prompt = e.target.getAttribute("data-prompt");
      promptInput.value = prompt;
      promptInput.focus();
      promptInput.style.height = "auto";
      promptInput.style.height = promptInput.scrollHeight + "px";
    }
  });
}

// Uncomment the line below to enable example prompts
// document.addEventListener('DOMContentLoaded', addExamplePrompts);
