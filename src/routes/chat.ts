import { Router, Request, Response } from "express";
import { initSSE, sendSSE, endSSE } from "../utils/sse.js";
import { errorResponse } from "../utils/response.js";
import { getModel } from "../models/modelRegistry.js";
import { OllamaProvider } from "../providers/ollama.js";
import { OpenAIProvider } from "../providers/openai.js";
import { GeminiProvider } from "../providers/gemini.js";

const router = Router();

function pickProvider(providerName: string) {
  switch (providerName) {
    case "openai": return new OpenAIProvider();
    case "gemini": return new GeminiProvider();
    default: return new OllamaProvider();
  }
}

router.post("/", async (req: Request, res: Response) => {
  const { messages, model, stream } = req.body;

  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json(errorResponse("Invalid messages array"));
  }

  const info = getModel(model);
  const provider = pickProvider(info.provider);

  if (stream !== false) {
    initSSE(res);
    try {
      await provider.stream(messages, chunk => sendSSE(res, { chunk }));
      endSSE(res);
    } catch (err: any) {
      sendSSE(res, { error: err.message });
      endSSE(res);
    }
  } else {
    try {
      const output = await provider.complete(messages);
      res.json({ text: output });
    } catch (err: any) {
      res.status(500).json(errorResponse(err.message));
    }
  }
});

export default router;

