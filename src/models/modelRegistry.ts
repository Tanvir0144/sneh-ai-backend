export const SNEH_MODELS = {
  "sneh-2.5-flash": {
    title: "Sneh 2.5 Flash",
    description: "Fast and lightweight model for summaries, translation, quick help.",
    provider: "ollama",
    engine: "llama3.1:8b",
    tier: "free",
  },
  "sneh-2.5-pro": {
    title: "Sneh 2.5 Pro",
    description: "Advanced reasoning, writing, and logic tasks.",
    provider: "openai",
    engine: "gpt-4o-mini",
    tier: "pro",
  },
  "sneh-plus": {
    title: "Sneh Plus",
    description: "Multimodal AI for text, image, voice & code.",
    provider: "gemini",
    engine: "gemini-1.5-pro",
    tier: "pro",
  },
};

export type SnehModelKey = keyof typeof SNEH_MODELS;

export function getModel(key: SnehModelKey) {
  return SNEH_MODELS[key] || SNEH_MODELS["sneh-2.5-flash"];
}

