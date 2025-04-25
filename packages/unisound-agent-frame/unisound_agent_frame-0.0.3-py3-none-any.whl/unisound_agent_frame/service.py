import argparse
import asyncio
import multiprocessing

from unisound_agent_frame.base.framework import Framework

async def main():
    # 创建框架实例并启动服务
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="dev", choices=["dev","uat","prod"], help="运行环境（dev/uat/prod）")
    args = parser.parse_args()

    # 根据环境计算 workers 数量
    if args.env == "prod":
        # 生产环境：CPU核心数 × 2
        workers = multiprocessing.cpu_count() * 2
    else:
        # 开发环境：固定为 1
        workers = 1

    # 创建框架实例并启动服务，传递 workers 参数
    framework = Framework()
    try:
        await framework.start(workers=workers)  # 直接传递计算后的 workers 值
    except KeyboardInterrupt:
        await framework.shutdown("shutdown")

if __name__ == "__main__":
    asyncio.run(main())