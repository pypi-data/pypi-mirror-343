def run_mcp():
    import asyncio
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("ClickMCP")

    @mcp.tool()
    def find_chart_by_name(name: str) -> str:
        """이름으로 차트를 찾습니다."""

        if name == "김길동":
            return "00000001"
        elif name == "홍길동":
            return "00000002"

        return "차트를 찾을 수 없습니다."

    # asyncio.run(mcp.run_stdio_async())
    asyncio.run(mcp.run_sse_async())


if __name__ == "__main__":
    run_mcp()
