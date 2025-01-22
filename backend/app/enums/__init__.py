from enum import Enum as PyEnum

class Role(str, PyEnum):
    user = "user"
    admin = "admin"

class RequestStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class IssueType(str, PyEnum):
    bug = "bug_report"
    feature = "feature_request"
    general = "general_inquiry"
