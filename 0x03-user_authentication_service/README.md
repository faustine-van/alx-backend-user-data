# 0x03. User authentication service
`Back-end`   `Authentification`

### Setup
You will need to install bcrypt
```
pip3 install bcrypt
```

Install SQLAlchemy module version 1.4.x
```
pip3 install SQLAlchemy
```
### Tasks
Task0. User model
[mapping declaration of SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping)

Task1. create user
```
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
```

## Run
```
$ chmod a+x main.py
$ python3 main.py
```

### Reference 
1. [REST API Authentication Mechanisms](https://www.youtube.com/watch?v=501dpx2IjGY)
2. [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
3. [Base64 concepts.](https://docs.python.org/3/library/base64.html?utm_campaign=ALX+-+2023+-+SE+Cohort+13&utm_medium=email&_hsmi=82680881&_hsenc=p2ANqtz-9IE9hfhkVUI85UMieLP96s3-xDU4NyVRgHzNy1fb5rjQFiIWIF6aNlbEfke9o2kRvkJgaEkmK0i7aTy1a3-B7v3Zvgxny9b0aKWX80iYE2QyBgSQY&utm_content=82680881&utm_source=hs_email#module-base64)
4. [HTTP status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
5. [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
5. [Requests module](https://requests.kennethreitz.org/en/latest/user/quickstart/)
6. [Python-Flask: Flask-User](https://flask-httpauth.readthedocs.io/en/latest/)
