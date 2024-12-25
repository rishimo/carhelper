from server.app import app
from server.routes.auth import router as AuthRouter
from server.routes.register import router as RegisterRouter
from server.routes.user import router as UserRouter

app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(RegisterRouter)
