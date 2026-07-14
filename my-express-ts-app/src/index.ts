import express, { Request, Response } from 'express';
import userRoutes from './routes/user.route';
import cors from 'cors';

// BigInt 직렬화 처리 (Prisma BigInt 타입이 res.json에서 에러나는 것 방지)
(BigInt.prototype as any).toJSON = function () {
    return this.toString();
};

const app = express();
const port = 3000;

//cors
app.use(cors());

//json 설정
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



app.use('/api/user', userRoutes);


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});