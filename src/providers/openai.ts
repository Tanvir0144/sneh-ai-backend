import { Provider, ChatMessage } from "./provider.js";
import OpenAI from "openai";
import { loadEnv } from "../utils/env.js";

const env = loadEnv();

export class OpenAIProvider implements Provider {
  name = "openai";
  client = new OpenAI({ apiKey: env.OPENAI_API_KEY });

  async stream(messages: ChatMessage[], onChunk: (chunk: string) => void) {
    const stream = await this.client.chat.completions.create({
      model: "gpt-4o-mini",
      messages,
      stream: true,
    });

    for await (const part of stream) {
      const delta = part.choices[0]?.delta?.content || "";
      if (delta) onChunk(delta);
    }
  }

  async complete(messages: ChatMessage[]) {
    const res = await this.client.chat.completions.create({
      model: "gpt-4o-mini",
      messages,
    });
    return res.choices[0]?.message?.content || "";
  }
}

