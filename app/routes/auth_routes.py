from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def read_root():
    return {
        "Mensagem": "Você acessou a pagina de autenticação!",
        "Autencicação": False
        }