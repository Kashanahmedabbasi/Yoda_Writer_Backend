from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import engine
import models
from routers.User import user
from routers.Category import category
from routers.SubCategory import subcategory
from routers.Packages import packages
from routers.DashboardAPIs import dashboard
from routers.Subscription import subscription

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user.router)
app.include_router(dashboard.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(packages.router)
app.include_router(subscription.router)

origins = ["*"]
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

if __name__=='__main__':
    uvicorn.run(app=app, host='192.168.18.106', port=9000)