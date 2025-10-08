import express from "express";
import cors from "cors";
import { limiter } from "./utils/limiter.js";
import { loadEnv } from "./utils/env.js";
import { okResponse } from "./utils/response.js";

import healthRoute from "./routes/health.js";
import modelsRoute from "./routes/models.js";
import chatRoute from "./routes/chat.js";

const env = loadEnv();
const app = express();

app.use(express.json({ limit: "2mb" }));
app.use(cors({ origin: env.CORS_ORIGIN || "*", credentials: false }));
app.use(limiter);

app.get("/", (_, res) => {
  res.json(okResponse("Welcome to Sneh Ai Backend 🚀"));
});

app.use("/api/health", healthRoute);
app.use("/api/models", modelsRoute);
app.use("/api/chat", chatRoute);

app.listen(env.PORT, () => {
  console.log(`✅ Sneh Ai backend running on http://localhost:${env.PORT}`);
});
