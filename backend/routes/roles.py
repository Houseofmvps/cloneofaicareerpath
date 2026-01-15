"""
Roles routes - AI/ML Role definitions and endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from data.roles import AI_ROLES, GLOBAL_HIRING

router = APIRouter(tags=["roles"])


@router.get("/roles")
async def get_roles(location: Optional[str] = Query(None, description="Filter salaries by location: us, india, europe, brazil, se_asia")):
    """Get all AI roles with optional location-specific salary filtering"""
    if location:
        location = location.lower()
        roles_with_local_salary = []
        for role in AI_ROLES:
            role_copy = role.copy()
            if "salary" in role and location in role["salary"]:
                role_copy["local_salary"] = role["salary"][location]
            roles_with_local_salary.append(role_copy)
        return {"roles": roles_with_local_salary, "location": location}
    return {"roles": AI_ROLES}


@router.get("/roles/{role_id}")
async def get_role(role_id: str, location: Optional[str] = Query(None)):
    """Get specific role with full details"""
    role = next((r for r in AI_ROLES if r["id"] == role_id), None)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    response = role.copy()
    if location and "salary" in role:
        location = location.lower()
        if location in role["salary"]:
            response["local_salary"] = role["salary"][location]
    
    response["hiring_patterns"] = GLOBAL_HIRING
    return response


@router.get("/hiring-patterns")
async def get_hiring_patterns():
    """Get global hiring patterns for AI roles"""
    return {"hiring_patterns": GLOBAL_HIRING}
