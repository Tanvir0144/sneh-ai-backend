import { Router } from "express";
import { okResponse } from "../utils/response.js";
import { SNEH_MODELS } from "../models/modelRegistry.js";

const router = Router();

router.get("/", (_, res) => {
  res.json(okResponse("Available models", SNEH_MODELS));
});

export default router;

