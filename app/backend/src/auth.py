from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status


@dataclass
class UserContext:
    user_id: str
    role: str
    org_id: str


ORGS = {
    "org-1": {"id": "org-1", "name": "Acme Security"},
    "org-2": {"id": "org-2", "name": "Globex Labs"},
}
# In production, org/user data would come from Supabase/Postgres with RLS policies.


def reset_orgs() -> None:
    ORGS.clear()
    ORGS.update(
        {
            "org-1": {"id": "org-1", "name": "Acme Security"},
            "org-2": {"id": "org-2", "name": "Globex Labs"},
        }
    )


def get_current_user(
    x_user_id: str | None = Header(default=None),
    x_role: str | None = Header(default=None),
    x_org_id: str | None = Header(default=None),
) -> UserContext:
    if not x_user_id or not x_role or not x_org_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication headers",
        )

    if x_role not in {"admin", "analyst", "billing"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unknown role")

    return UserContext(user_id=x_user_id, role=x_role, org_id=x_org_id)


def require_admin_user(user: UserContext = Depends(get_current_user)) -> UserContext:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


def assert_org_access(request_org_id: str, user: UserContext) -> None:
    if user.role == "admin":
        return
    if request_org_id != user.org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-org access denied",
        )
