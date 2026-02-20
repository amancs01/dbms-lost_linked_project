# LostLinked - Quick Start Guide

Get up and running with LostLinked in 5 minutes!

## Prerequisites

- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ PostgreSQL database (local or cloud service like [Neon](https://neon.tech) or [Supabase](https://supabase.com))

## Step 1: Set Up Database

### Option A: Using Neon (Recommended - Free PostgreSQL)

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy the connection string (looks like: `postgresql://user:pass@host/db`)

### Option B: Local PostgreSQL

```bash
# Create database
createdb lostlinked

# Your connection string will be:
# postgresql://localhost/lostlinked
```

## Step 2: Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Copy environment file
cp .env.example .env

# Edit .env and paste your database URL
# DATABASE_URL=postgresql://your-connection-string-here
# SECRET_KEY=your-secret-key-minimum-32-characters-long

# For Linux/macOS:
chmod +x run.sh
./run.sh

# For Windows:
run.bat

# OR manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start at `http://localhost:8000` ✅

## Step 3: Frontend Setup (Terminal 2)

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at `http://localhost:5173` ✅

## Step 4: Test the Application

1. Open `http://localhost:5173` in your browser
2. You should see the LostLinked homepage with empty Lost/Found sections
3. Click "Report Lost" or "Report Found" to add test items
4. Click "Admin Login" and use:
   - **Username:** `admin`
   - **Password:** `admin123`
5. Once logged in, you'll see delete buttons on items

## Quick Test Data

Here's some test data you can enter:

### Lost Item Example
- **Item Name:** iPhone 13 Pro
- **Description:** Black iPhone 13 Pro with a blue case
- **Category:** Electronics
- **Date:** Today's date
- **Location:** Main Library, 2nd Floor
- **Your Name:** John Doe
- **Contact:** john.doe@email.com

### Found Item Example
- **Item Name:** Blue Backpack
- **Description:** Small blue backpack with laptop compartment
- **Category:** Bags
- **Date:** Today's date
- **Location:** Cafeteria
- **Your Name:** Jane Smith
- **Contact:** jane.smith@email.com

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### "Connection refused" error
- Make sure PostgreSQL is running
- Check your DATABASE_URL in .env

### "Module not found" error
- Backend: Make sure virtual environment is activated
- Frontend: Run `npm install` again

### Port already in use
- Backend (8000): Kill the process or change port in main.py
- Frontend (5173): Kill the process or change port in vite.config.js

### CORS errors
- Make sure backend is running on port 8000
- Check the API_BASE_URL in frontend/src/services/api.js

## Next Steps

- ✅ Customize the categories in ReportForm.jsx
- ✅ Change default admin credentials
- ✅ Add more users to the database
- ✅ Customize the UI colors and styling
- ✅ Deploy to production (see README.md)

## Common Commands

### Backend
```bash
# Start server
python main.py

# With auto-reload
uvicorn main:app --reload

# Run on different port
uvicorn main:app --port 8080
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Need Help?

- 📖 Full documentation: See `README.md`
- 🐛 Found a bug? Open an issue
- 💡 Have questions? Check the API docs at `/docs`

---

Happy coding! 🎉
