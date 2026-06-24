"""Placeholder route handlers

This module contains placeholder route handlers for Sprint 0.
Routes will be fully implemented in subsequent sprints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint - placeholder"""
    return {"message": "LIPU API - Placeholder route"}
