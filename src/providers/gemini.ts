import { Provider, ChatMessage } from "./provider.js";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { loadEnv } from "../utils/env.js";

const env = loadEnv();

export class GeminiProvider implements Provider {
  name = "gemini";
  genAI = new GoogleGenerativeAI(env.GEMINI_API_KEY);

  async stream(messages: ChatMessage[], onChunk: (chunk: string) => void) {
    const model = this.genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
    const history = messages.map(m => ({
      role: m.role === "user" ? "user" : "model",
      parts: [{ text: m.content }],
    }));
    const chat = model.startChat({ history: history.slice(0, -1) });
    const last = messages[messages.length - 1]?.content || "";
    const res = await chat.sendMessageStream(last);

    for await (const chunk of res.stream) {
      const text = chunk.text();
      if (text) onChunk(text);
    }
  }

  async complete(messages: ChatMessage[]) {
    let text = "";
    await this.stream(messages, chunk => (text += chunk));
    return text;
  }
}

