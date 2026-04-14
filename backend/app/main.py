from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.produto_router import router as produto_router
from app.routers.consumidor import router as consumidor_router
from app.routers.vendedor import router as vendedor_router
from app.routers.pedido import router as pedido_router
from app.routers.item_pedido import router as item_pedido_router
from app.routers.avaliacao_pedido import router as avaliacao_pedido_router

app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


app.include_router(produto_router)
app.include_router(consumidor_router)
app.include_router(vendedor_router)
app.include_router(pedido_router)
app.include_router(item_pedido_router)
app.include_router(avaliacao_pedido_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)