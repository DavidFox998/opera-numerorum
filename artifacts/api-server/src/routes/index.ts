import { Router, type IRouter } from "express";
import healthRouter from "./health";
import verifyRouter from "./verify";
import certsRouter from "./certs";

const router: IRouter = Router();

router.use(healthRouter);
router.use(verifyRouter);
router.use(certsRouter);

export default router;
