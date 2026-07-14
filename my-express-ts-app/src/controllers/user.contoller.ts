import { Request, Response } from 'express';
import { PrismaClient } from '../generated/prisma/client';

const prisma = new PrismaClient({});


//address로 회원 조회
export const getUserByAddress = async (req: Request, res: Response): Promise<Response> => {
    const { address } = req.params;
    const user = await prisma.user.findMany({
        where: { address: address as string }
    });
    return res.status(200).json({
        success: true,
        message: '회원 조회 성공',
        data: user
    });
};


//nick으로 회원 조회
export const getUserByNick = async (req: Request, res: Response): Promise<Response> => {
    const { nick } = req.params;
    const user = await prisma.user.findUnique({
        where: { nick: nick as string }
    });
    return res.status(200).json({
        success: true,
        message: '회원 조회 성공',
        data: user
    });
};

//idx로 회원 조회
export const getUserById = async (req: Request, res: Response): Promise<Response> => {
    const { idx } = req.params;
    const user = await prisma.user.findUnique({
        where: { idx: parseInt(idx as string) }
    });
    return res.status(200).json({
        success: true,
        message: '회원 조회 성공',
        data: user
    });
};

//회원가입
export const signup = async (req: Request, res: Response): Promise<Response> => {
    const { id, pw, nick, address } = req.body;
    const user = await prisma.user.create({
        data: {
            id,
            pw,
            nick,
            address,
            created_at: new Date(),
            updated_at: new Date(),
            is_active: 'Y',
            point: 0
        }
    });

    return res.status(200).json({
        success: true,
        message: '회원가입 성공',
        data: user
    });
};

export const testMethod = (req: Request, res: Response) => {
    res.send('Hello, TypeScript with Express! test');
};

