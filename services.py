import database as _database
import models as _models
import sqlalchemy.orm as _orm

import schemas as _schemas
import email_validator as _email_validator
import fastapi as _fastapi
import passlib.hash as _hash


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def getUserByEmail(email: str, db: _orm.Session):
    return db.query(_models.UserModel).filter(_models.UserModel.email == email).first()


async def create_user(user: _schemas.UserRequest, db: _orm.Session):
    # check for valid email
    try:
        isvalid = _email_validator.validate_email(email=user.email)
        email = isvalid.email
    except _email_validator.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=400, detail="Provide valid Email")

    hashed_password = _hash.bcrypt.hash(user.password)
    # create the user model to be saved in database
    user_object = _models.UserModel(
        email=email,
        name=user.name,
        phone=user.phone,
        password_hash=hashed_password
    )
    # save the user in the db
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object


