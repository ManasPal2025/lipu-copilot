"""Product catalog endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.schemas.pagination import Page
from app.schemas.product import (
    ProductCreate,
    ProductDetailRead,
    ProductRead,
    ProductSort,
    ProductStatus,
    ProductUpdate,
    ProductVisibility,
)
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryRead, ProductCategoryUpdate
from app.schemas.product_variant import ProductVariantCreate, ProductVariantCreateForProduct, ProductVariantRead, ProductVariantUpdate
from app.services.product_catalog import ProductCatalogService


router = APIRouter(prefix="/catalog", tags=["product-catalog"])


def get_product_catalog_service(session: AsyncSession = Depends(get_session)) -> ProductCatalogService:
    return ProductCatalogService(session)


@router.get("/categories", response_model=Page[ProductCategoryRead])
async def list_categories(
    organization_id: UUID | None = Query(default=None),
    parent_category_id: UUID | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Page[ProductCategoryRead]:
    return await service.list_categories(
        organization_id=organization_id,
        parent_category_id=parent_category_id,
        is_active=is_active,
        offset=offset,
        limit=limit,
    )


@router.post("/categories", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: ProductCategoryCreate,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductCategoryRead:
    return await service.create_category(payload)


@router.get("/categories/{category_id}", response_model=ProductCategoryRead)
async def get_category(
    category_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductCategoryRead:
    return await service.get_category(category_id)


@router.patch("/categories/{category_id}", response_model=ProductCategoryRead)
async def update_category(
    category_id: UUID,
    payload: ProductCategoryUpdate,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductCategoryRead:
    return await service.update_category(category_id, payload)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Response:
    await service.delete_category(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/products", response_model=Page[ProductRead])
async def list_products(
    organization_id: UUID | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    status_filter: ProductStatus | None = Query(default=None, alias="status"),
    visibility: ProductVisibility | None = Query(default=None),
    is_bestseller: bool | None = Query(default=None),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    sort: ProductSort = Query(default="-created_at"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Page[ProductRead]:
    return await service.list_products(
        organization_id=organization_id,
        category_id=category_id,
        status=status_filter,
        visibility=visibility,
        is_bestseller=is_bestseller,
        min_price=min_price,
        max_price=max_price,
        search=search,
        sort=sort,
        offset=offset,
        limit=limit,
    )


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductRead:
    return await service.create_product(payload)


@router.get("/products/{product_id}", response_model=ProductDetailRead)
async def get_product(
    product_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductDetailRead:
    return await service.get_product(product_id, include_variants=True)


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductRead:
    return await service.update_product(product_id, payload)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Response:
    await service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/products/{product_id}/variants", response_model=Page[ProductVariantRead])
async def list_product_variants(
    product_id: UUID,
    variant_type: str | None = Query(default=None, min_length=1, max_length=50),
    is_available: bool | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Page[ProductVariantRead]:
    return await service.list_variants(
        product_id=product_id,
        variant_type=variant_type,
        is_available=is_available,
        offset=offset,
        limit=limit,
    )


@router.post("/products/{product_id}/variants", response_model=ProductVariantRead, status_code=status.HTTP_201_CREATED)
async def create_product_variant(
    product_id: UUID,
    payload: ProductVariantCreateForProduct,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductVariantRead:
    create_payload = ProductVariantCreate(product_id=product_id, **payload.model_dump())
    return await service.create_variant(create_payload)


@router.get("/variants/{variant_id}", response_model=ProductVariantRead)
async def get_variant(
    variant_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductVariantRead:
    return await service.get_variant(variant_id)


@router.patch("/variants/{variant_id}", response_model=ProductVariantRead)
async def update_variant(
    variant_id: UUID,
    payload: ProductVariantUpdate,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> ProductVariantRead:
    return await service.update_variant(variant_id, payload)


@router.delete("/variants/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(
    variant_id: UUID,
    service: ProductCatalogService = Depends(get_product_catalog_service),
) -> Response:
    await service.delete_variant(variant_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
