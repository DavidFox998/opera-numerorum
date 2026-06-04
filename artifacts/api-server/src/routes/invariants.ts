import { Router, type IRouter } from "express";
import path from "path";
import fs from "fs";

const router: IRouter = Router();

const INVARIANTS_PATH = path.resolve(
  process.cwd(),
  "../../certificates/invariants.json",
);

router.get("/invariants", (_req, res) => {
  if (!fs.existsSync(INVARIANTS_PATH)) {
    res.status(404).json({ error: "invariants.json not found" });
    return;
  }
  try {
    const raw = fs.readFileSync(INVARIANTS_PATH, "utf-8");
    const data = JSON.parse(raw);
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Failed to read invariants.json" });
  }
});

export default router;
