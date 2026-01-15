"""
Data package - Contains core data structures
"""
from data.roles import AI_ROLES, GLOBAL_HIRING, get_role_by_id, get_all_role_ids
from data.courses import COURSE_DATABASE, get_courses_for_role, get_scrimba_courses, get_free_courses
from data.pricing import PRICING, FREE_LIMITS, get_feature_limit, get_pricing_info

__all__ = [
    # Roles
    "AI_ROLES",
    "GLOBAL_HIRING",
    "get_role_by_id",
    "get_all_role_ids",
    # Courses
    "COURSE_DATABASE",
    "get_courses_for_role",
    "get_scrimba_courses",
    "get_free_courses",
    # Pricing
    "PRICING",
    "FREE_LIMITS",
    "get_feature_limit",
    "get_pricing_info"
]
