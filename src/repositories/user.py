from sqlalchemy.orm import Session

from src.models.user import User


def get_user_index(db: Session, user_id: int):
    return db.query(User.user_index).filter(User.user_id == user_id).one()[0]


def get_group_user_index(db: Session, user_ids: list[int]):
    result = (db.query(User.user_index)
              .filter(User.user_id.in_(user_ids), User.user_index != None).all())
    user_ids = []
    for t in result:
        user_ids.append(t[0])
    return user_ids
