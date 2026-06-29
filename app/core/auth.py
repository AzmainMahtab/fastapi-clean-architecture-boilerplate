"""Cross-module re-exports for authentication guards.

Other modules (e.g. ``user``, ``admin``) should import auth guard
dependencies from here rather than directly from
``app.modules.auth.api.dependencies`` to avoid crossing module
boundaries and violating encapsulation boundaries within the
modular monolith.
"""

from app.modules.auth.api.dependencies import require_authenticated, require_authenticated_user

__all__ = ["require_authenticated", "require_authenticated_user"]
