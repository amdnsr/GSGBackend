# GetSeatGoBackend

This project aims to serve as the backend for the GetSeatGo App

## Requirements

To run the service, create a virtual environment and install the requirements by running the following command:

```setup
pip install -r requirements.txt
```

## Usage

Either export the following **configurations** `environment variables` or set their values in config.json
```usage
export "TITLE"="GetSeatGo",
export "VERSION"="0.0.1"
export "DESCRIPTION"="Backend for GetSeatGo App"
export "HOST"="0.0.0.0"
export "PORT"=8080
export "RELOAD"=true
export "DEBUG"=true # only in case of debugging, in production, it to false
```

Similarly, either export the following **settings** `environment variables` or set their values in settings.json
```usage
export "ALGORITHM"=<ALGORITHM>
export "SECRET_KEY"=<SECRET_KEY>
export "ENVIRONMENT"=<DEV/PYTEST/STAGE/PRODUCTION>
export "ACCESS_TOKEN_EXPIRE_MINUTES"=<ACCESS_TOKEN_EXPIRE_MINUTES>
export "REFRESH_TOKEN_EXPIRE_MINUTES"=<REFRESH_TOKEN_EXPIRE_MINUTES>
export "BACKEND_CORS_ORIGINS"=<BACKEND_CORS_ORIGINS>

```

* Note: If a variable's value is set in both the environment and config/settings.json, the value in the environment will take precedence 

Finally, run the project using:
```
python main.py
```
