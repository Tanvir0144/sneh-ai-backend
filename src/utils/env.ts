// Sneh ai

import "dotenv/config";

export function loadEnv() {
  return {
    PORT: process.env.PORT || 8787,
    CORS_ORIGIN: process.env.CORS_ORIGIN || "*",

    // Providers
    OLLAMA_BASE_URL: process.env.OLLAMA_BASE_URL || "http://localhost:11434",
    OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
    GEMINI_API_KEY: process.env.GEMINI_API_KEY || "",

    // Default Models
    DEFAULT_MODEL: process.env.DEFAULT_MODEL || "sneh-2.5-flash",
  };
}
