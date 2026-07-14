import { Router } from 'express';
import { testMethod } from '../controllers/user.contoller';

const router = Router();

router.get('/test', testMethod);

export default router;