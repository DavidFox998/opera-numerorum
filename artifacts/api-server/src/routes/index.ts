import { Router, type IRouter } from "express";
import healthRouter from "./health";
import verifyRouter from "./verify";
import certsRouter from "./certs";
import invariantsRouter from "./invariants";

const router: IRouter = Router();

router.use(healthRouter);
router.use(verifyRouter);
router.use(certsRouter);
router.use(invariantsRouter);

export default router;
