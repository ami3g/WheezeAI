from sqlalchemy.orm import Session
from backend.models.organization_invite import OrganizationInvite
from backend.schemas.organization_invite import OrganizationInviteCreate

def create_invite(db: Session, invite: OrganizationInviteCreate) -> OrganizationInvite:
    db_invite = OrganizationInvite(
        organization_id=invite.organization_id,
        email=invite.email
    )
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite


def get_invite(db: Session, invite_id: int) -> OrganizationInvite | None:
    return db.query(OrganizationInvite).filter(OrganizationInvite.id == invite_id).first()


def list_invites(db: Session, organization_id: int) -> list[OrganizationInvite]:
    return db.query(OrganizationInvite).filter(OrganizationInvite.organization_id == organization_id).all()


def accept_invite(db: Session, invite_id: int, user_id: int) -> OrganizationInvite | None:
    invite = get_invite(db, invite_id)
    if invite and invite.status == "pending":
        invite.status = "accepted"
        db.commit()
        db.refresh(invite)
        # Add user to organization
        from backend.models.user_organization import UserOrganization
        db_user_org = UserOrganization(user_id=user_id, organization_id=invite.organization_id)
        db.add(db_user_org)
        db.commit()
        db.refresh(db_user_org)
        return invite
    return None
