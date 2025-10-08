export type ChatMessage = { role: "system" | "user" | "assistant"; content: string };

export interface Provider {
  name: string;
  stream(messages: ChatMessage[], onChunk: (chunk: string) => void): Promise<void>;
  complete(messages: ChatMessage[]): Promise<string>;
}

