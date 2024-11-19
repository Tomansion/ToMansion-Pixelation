# ToMansion Pixelation

Yet another r/place clone.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-1c4a6c.svg)](https://flake8.pycqa.org/en/latest/)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

![ci](https://github.com/tomansion/Vue3-FastAPI-WebApp-template/actions/workflows/pull-request-checks.yml/badge.svg)
![cd](https://github.com/tomansion/Vue3-FastAPI-WebApp-template/actions/workflows/continuous-deployment.yml/badge.svg)

---

This project was made from the [Vue3-FastAPI-WebApp-template](https://github.com/Tomansion/Vue3-FastAPI-WebApp-template/)

## Running the application in development mode

#### Prerequisites

- [Python](https://www.python.org/downloads/) v3.9+ for the backend.
- [Node.js](https://nodejs.org/en/download/) v19.0.0c and [npm](https://www.npmjs.com/get-npm) v8.19.2 for the frontend.

1. Clone the repository:

```bash
git clone https://github.com/Tomansion/ToMansion-Pixelation
cd ToMansion-Pixelation
```

2. Install the backend and frontend dependencies:

```bash
make install

# Or manually:
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
```

3. Run the backend and frontend:

```bash
make run

# Or manually:
cd backend
uvicorn websrv:app --reload --host 0.0.0.0 --port 3000
cd frontend # In another terminal
npm run serve
```

5. Open the App:

- The application frontend: [http://localhost:8080](http://localhost:8080)
- The FastAPI backend: [http://localhost:3000](http://localhost:3000)
- The API SwaggerUI documentation: [http://localhost:3000/docs](http://localhost:3000/docs)
- The API Redoc documentation: [http://localhost:3000/redoc](http://localhost:3000/docs)

## Help

If you have any questions or need help, feel free to [open an issue](https://github.com/Tomansion/ToMansion-Pixelation/issues/).

## Contributing

I'm open to contributions and suggestions. Feel free to [open an issue](https://github.com/Tomansion/Vue3-FastAPI-WebApp-template/issues) or a make a pull request.
