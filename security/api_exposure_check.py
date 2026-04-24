#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path


def has_admin_dependency(func: ast.FunctionDef) -> bool:
    args = func.args
    defaults = args.defaults
    for default in defaults:
        if isinstance(default, ast.Call) and isinstance(default.func, ast.Name):
            if default.func.id == "Depends" and default.args:
                first_arg = default.args[0]
                if isinstance(first_arg, ast.Name) and first_arg.id == "require_admin_user":
                    return True
    return False


def is_admin_route(decorator: ast.expr) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    if not isinstance(decorator.func, ast.Attribute):
        return False
    if decorator.func.attr not in {"get", "post", "delete", "put", "patch"}:
        return False
    if not decorator.args:
        return False
    route_arg = decorator.args[0]
    return isinstance(route_arg, ast.Constant) and str(route_arg.value).startswith("/api/admin")


def main() -> int:
    target = Path(__file__).resolve().parents[1] / "app/backend/src/main.py"
    tree = ast.parse(target.read_text(encoding="utf-8"))

    violations: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if any(is_admin_route(d) for d in node.decorator_list):
                if not has_admin_dependency(node):
                    violations.append(node.name)

    if violations:
        print("ERROR: Admin endpoints missing require_admin_user dependency:")
        for item in violations:
            print(f"- {item}")
        return 1

    print("API exposure check passed: admin routes require authenticated admin context.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
