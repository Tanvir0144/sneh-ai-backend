import rateLimit from "express-rate-limit";

export const limiter = rateLimit({
  windowMs: 15 * 1000, // 15 sec window
  max: 60, // 60 reqs per window
  standardHeaders: "draft-7",
  legacyHeaders: false,
});
