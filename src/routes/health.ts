import { Router } from "express";
import { okResponse } from "../utils/response.js";
const router = Router();

router.get("/", (_, res) => {
  res.json(okResponse("Sneh Ai Backend is healthy ✅"));
});

export default router;
