import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()


@app.post("/api/v1/users")
async def register_user(
        user: _schemas.UserRequest, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    # call to check if user with email exist
    db_user = await _services.getUserByEmail(email=user.email, db=db)
    # if user is found throw exception
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already exist, try with another email")

    # create the user and return a token
    db_user = await _services.create_user(user=user, db=db)
    return await _services.create_token(user=db_user)


@app.post("/api/v1/login")
async def login_user(
        form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.login(email=form_data.username,
                                    password=form_data.password, db=db)
    # Invalid login then throw exception
    if not db_user:
        raise _fastapi.HTTPException(status_code=401, detail="Wrong Login Credentials")
    # create and return token
    return await _services.create_token(db_user)