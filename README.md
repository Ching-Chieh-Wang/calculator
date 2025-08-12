# Calculator App

A simple calculator with a **Vue 3 + Tailwind CSS frontend** and a **Flask backend**.

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on [http://localhost:5173](http://localhost:5173).

---

## Backend Setup

1. **Go to backend folder**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   python app.py
   ```

The backend will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Notes

- The frontend communicates with the backend through API routes under `/api`.
- Ensure the backend is running before using the calculator UI.
- If running both together, start the backend first, then the frontend.
