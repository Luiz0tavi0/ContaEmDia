from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.financial_category import make_financial_category
from src.crud.user import UserCRUD
from src.db.session import get_session
from src.models.base import DeleteResponse
from src.models.financial_category import FinancialCategory
from src.models.user import UserCreate, User, UserResponse

# from src.models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", summary="Create a new user.", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user_route(
        data: UserCreate,
        db: AsyncSession = Depends(get_session),
):
    return await UserCRUD.create(db, data)


@router.post("/ct_fin", summary="Create a new category finance.", status_code=status.HTTP_201_CREATED,
             response_model=FinancialCategory)
async def create_financial_category(
        data: FinancialCategory,
        db: AsyncSession = Depends(get_session),
):
    return await make_financial_category(db, data)


# @router.get("/{id}", summary="Get a user.", status_code=status.HTTP_200_OK, response_model=UserResponse):
# async def get_user_route(id: UUID, db: AsyncSession = Depends(get_session)):
    # return await get_user(session=db, id=id)


# @router.patch(
#     "/{id}",
#     summary="Update a user.",
#     status_code=status.HTTP_200_OK,
#     response_model=UserResponse,
# )
# async def update_user_route(
#         id: UUID,
#         data: UserUpdate,
#         db: AsyncSession = Depends(get_session),
# ):
#     return await update_user(session=db, id=id, user=data)


@router.delete("/{id}", summary="Delete a user.", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
async def delete_user_route(id: UUID, db: AsyncSession = Depends(get_session)):
    deleted = await UserCRUD.delete_by_id(session=db, user_id=id)
    return DeleteResponse(deleted=deleted)
