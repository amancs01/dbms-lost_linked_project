# LostLinked - Lost & Found Platform

A modern, full-stack web application for managing lost and found items. Built with FastAPI (Python) backend and React.js (Vite) frontend with a professional UI using Tailwind CSS.

## Features

### Backend (FastAPI)
- ✅ JWT-based authentication with secure password hashing
- ✅ PostgreSQL database with raw SQL queries (no ORM)
- ✅ RESTful API endpoints for CRUD operations
- ✅ CORS enabled for frontend integration
- ✅ Automatic database schema creation on startup
- ✅ Connection pooling for optimal performance

### Frontend (React + Vite)
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Authentication context with persistent sessions
- ✅ Protected routes for admin operations
- ✅ Real-time notifications with react-hot-toast
- ✅ Professional item cards with hover effects
- ✅ Separate forms for reporting lost/found items
- ✅ Two-column responsive grid layout

## Tech Stack

**Backend:**
- FastAPI
- PostgreSQL (psycopg2)
- JWT (python-jose)
- Bcrypt (passlib)
- Uvicorn

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- React Router DOM
- Axios
- React Hot Toast

## Project Structure

```
LostLinked/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Header.jsx
│   │   │   ├── ItemCard.jsx
│   │   │   ├── Spinner.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── ReportForm.jsx
│   │   │   └── LoginPage.jsx
│   │   ├── contexts/        # React contexts
│   │   │   └── AuthContext.jsx
│   │   ├── services/        # API services
│   │   │   └── api.js
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database (can use Neon, Supabase, or local PostgreSQL)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LostLinked
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your database credentials
# DATABASE_URL=postgresql://username:password@host:port/database
# SECRET_KEY=your-secret-key-here
```

### 3. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE lostlinked;
```

The application will automatically create the required tables on startup.

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Start the Backend Server

```bash
cd ../backend

# Make sure virtual environment is activated
# Run the FastAPI server
python main.py
# or
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 6. Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`

## Default Admin Credentials

```
Username: admin
Password: admin123
```

**⚠️ Important:** Change these credentials in production!

## API Endpoints

### Public Endpoints

- `GET /` - Root endpoint
- `POST /login` - Login and get JWT token
- `GET /lost-items` - Get all lost items
- `GET /found-items` - Get all found items
- `POST /lost-items` - Create a lost item report
- `POST /found-items` - Create a found item report

### Protected Endpoints (Requires Authentication)

- `DELETE /items/{item_type}/{item_id}` - Delete an item (lost or found)

## Database Schema

### lost_items
- `lost_id` (SERIAL PRIMARY KEY)
- `item_name` (VARCHAR)
- `description` (TEXT)
- `category` (VARCHAR)
- `lost_date` (VARCHAR)
- `location` (VARCHAR)
- `owner_name` (VARCHAR)
- `owner_contact` (VARCHAR)
- `status` (VARCHAR)

### found_items
- `found_id` (SERIAL PRIMARY KEY)
- `item_name` (VARCHAR)
- `description` (TEXT)
- `category` (VARCHAR)
- `found_date` (VARCHAR)
- `location` (VARCHAR)
- `finder_name` (VARCHAR)
- `finder_contact` (VARCHAR)
- `status` (VARCHAR)

### users
- `id` (SERIAL PRIMARY KEY)
- `username` (VARCHAR UNIQUE)
- `password` (VARCHAR - hashed)
- `role` (VARCHAR)

## Development

### Running Backend Tests

```bash
cd backend
pytest
```

### Building Frontend for Production

```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist` directory.

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/lostlinked
SECRET_KEY=your-super-secret-key-change-this-in-production
```

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Protected API endpoints
- ✅ CORS configuration
- ✅ SQL injection prevention through parameterized queries

## Features Walkthrough

### For Users (No Authentication Required)

1. **View Items**: Browse all lost and found items on the home page
2. **Report Lost Item**: Fill out the form to report a lost item
3. **Report Found Item**: Fill out the form to report a found item

### For Admins (Authentication Required)

1. **Login**: Access admin panel with credentials
2. **Delete Items**: Remove inappropriate or resolved items
3. **Manage Database**: Full control over item listings

## Customization

### Adding New Categories

Edit the categories array in `frontend/src/pages/ReportForm.jsx`:

```javascript
const categories = [
  'Electronics',
  'Clothing',
  'Accessories',
  'Documents',
  'Keys',
  'Bags',
  'YourNewCategory', // Add here
  'Other',
];
```

### Changing Color Scheme

Modify the Tailwind configuration in `frontend/tailwind.config.js`.

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists and credentials are correct

### CORS Errors

- Backend CORS is set to allow all origins (`*`) for development
- For production, update the `allow_origins` in `backend/main.py`

### Port Conflicts

- Backend default: `8000`
- Frontend default: `5173`
- Change ports in `vite.config.js` and when running uvicorn

## Production Deployment

### Backend

1. Set strong SECRET_KEY
2. Use production database (e.g., Neon, Supabase)
3. Configure CORS to specific origins
4. Use gunicorn or similar WSGI server
5. Set up HTTPS

### Frontend

1. Update API_BASE_URL in `frontend/src/services/api.js`
2. Build: `npm run build`
3. Deploy `dist` folder to hosting service (Vercel, Netlify, etc.)

## License

MIT License

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

Built with ❤️ using FastAPI and React
