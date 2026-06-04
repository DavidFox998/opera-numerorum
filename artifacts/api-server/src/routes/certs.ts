import { Router, type IRouter } from "express";
import path from "path";
import fs from "fs";

const router: IRouter = Router();

const CERTS_DIR = path.resolve(process.cwd(), "../../certificates");

router.get("/certs/:filename", (req, res) => {
  const filename = path.basename(req.params.filename);
  const isPdf = filename.endsWith(".pdf");
  const isSage = filename.endsWith(".sage");
  if (!isPdf && !isSage) {
    res.status(400).json({ error: "Only PDF and SAGE files are served." });
    return;
  }
  const filepath = path.join(CERTS_DIR, filename);
  if (!fs.existsSync(filepath)) {
    res.status(404).json({ error: "Certificate not found." });
    return;
  }
  if (isPdf) {
    res.setHeader("Content-Type", "application/pdf");
  } else {
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
  }
  res.setHeader("Content-Disposition", `attachment; filename="${filename}"`);
  res.sendFile(filepath);
});

export default router;
