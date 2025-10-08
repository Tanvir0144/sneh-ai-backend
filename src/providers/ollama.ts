import { Provider, ChatMessage } from "./provider.js";
import { loadEnv } from "../utils/env.js";

const env = loadEnv();

export class OllamaProvider implements Provider {
  name = "ollama";

  async stream(messages: ChatMessage[], onChunk: (chunk: string) => void) {
    // Native fetch (Node 22+)
    const res = await fetch(`${env.OLLAMA_BASE_URL}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3.1:8b",
        messages,
        stream: true,
      }),
    });

    if (!res.ok || !res.body) {
      throw new Error(`Ollama Error: ${res.status} ${res.statusText}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk
        .split("\n")
        .filter((line) => line.trim().startsWith("data:"));

      for (const line of lines) {
        const data = line.slice(5).trim();
        if (data === "[DONE]") return;
        try {
          const json = JSON.parse(data);
          const delta = json?.choices?.[0]?.delta?.content;
          if (delta) onChunk(delta);
        } catch {
          // Ignore malformed JSON
        }
      }
    }
  }

  async complete(messages: ChatMessage[]) {
    let fullText = "";
    await this.stream(messages, (chunk) => (fullText += chunk));
    return fullText;
  }
}
