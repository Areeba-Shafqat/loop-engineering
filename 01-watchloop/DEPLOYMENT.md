# WatchLoop Deployment Guide

## 🚀 Deployment Architecture

**Split Deployment (Recommended):**
- **Frontend** → Vercel (Static React app)
- **Backend** → Railway/Render/Heroku (Long-running Python server)

The backend requires a platform that supports long-running processes because the WatchLoop uses persistent threads that check task status every 60 seconds.

---

## 📦 Option 1: Vercel (Frontend) + Railway (Backend)

### **Step 1: Deploy Backend to Railway**

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `loop-engineering` repository
   - Select root path: `01-watchloop/backend`

3. **Configure Environment**
   - Railway will auto-detect Python and use `Procfile`
   - Add environment variable:
     ```
     PORT=5000
     WATCHLOOP_CHECK_INTERVAL=60
     ```

4. **Deploy**
   - Railway will automatically deploy
   - Note your backend URL: `https://your-app.up.railway.app`

### **Step 2: Deploy Frontend to Vercel**

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Configure Environment Variable**
   - Create `.env` file in frontend folder:
     ```
     VITE_API_URL=https://your-app.up.railway.app/api
     ```

3. **Deploy via Vercel Dashboard**
   - Visit https://vercel.com
   - Click "Add New Project"
   - Import `loop-engineering` repository
   - Set root directory: `01-watchloop/frontend`
   - Add environment variable:
     - Name: `VITE_API_URL`
     - Value: `https://your-app.up.railway.app/api`
   - Click "Deploy"

4. **Or Deploy via CLI**
   ```bash
   cd frontend
   vercel --prod
   ```

---

## 📦 Option 2: Render (Full-Stack)

Render can host both frontend and backend in one place.

### **Deploy Backend**

1. Visit https://render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Root Directory**: `01-watchloop/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_production.py`
   - **Environment Variables**:
     ```
     PORT=5000
     WATCHLOOP_CHECK_INTERVAL=60
     ```

### **Deploy Frontend**

1. Create new "Static Site"
2. Configure:
   - **Root Directory**: `01-watchloop/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variable**:
     ```
     VITE_API_URL=https://your-backend.onrender.com/api
     ```

---

## 📦 Option 3: Heroku (Backend) + Vercel (Frontend)

### **Deploy Backend to Heroku**

1. Install Heroku CLI
   ```bash
   npm install -g heroku
   ```

2. Login and create app
   ```bash
   heroku login
   cd 01-watchloop/backend
   heroku create watchloop-backend
   ```

3. Set environment variables
   ```bash
   heroku config:set WATCHLOOP_CHECK_INTERVAL=60
   ```

4. Deploy
   ```bash
   git init
   git add .
   git commit -m "Deploy backend"
   git push heroku master
   ```

5. Note your backend URL: `https://watchloop-backend.herokuapp.com`

### **Deploy Frontend to Vercel**
- Follow Step 2 from Option 1 above

---

## 🔧 Backend Configuration Updates Needed

### **1. Update CORS for Production**

Edit `backend/app.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://*.vercel.app",
    "https://yourdomain.com"
])
```

### **2. Use PORT from Environment**

Edit `backend/run_production.py`:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
```

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Update CORS settings in backend
- [ ] Set PORT environment variable support
- [ ] Configure VITE_API_URL in frontend
- [ ] Test locally with production build
- [ ] Deploy backend first
- [ ] Update frontend with backend URL
- [ ] Deploy frontend
- [ ] Test live deployment end-to-end

---

## 🧪 Test Production Build Locally

### **Backend**
```bash
cd 01-watchloop/backend
export PORT=5000
python run_production.py
```

### **Frontend**
```bash
cd 01-watchloop/frontend
npm run build
npm run preview
```

Visit http://localhost:4173 to test

---

## 🔐 Environment Variables Reference

### **Backend**
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Server port |
| `WATCHLOOP_CHECK_INTERVAL` | 60 | Check interval in seconds |

### **Frontend**
| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | http://localhost:5000/api | Backend API URL |

---

## 🌐 Custom Domain (Optional)

### **Vercel Frontend**
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### **Railway Backend**
1. Go to Project Settings → Domains
2. Add custom domain
3. Configure CNAME record

---

## 📊 Monitoring

### **Railway**
- View logs in dashboard
- Monitor CPU/Memory usage
- Set up alerts

### **Vercel**
- Analytics in dashboard
- Function logs
- Performance metrics

---

## 💰 Cost Estimates

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| **Vercel** | Unlimited hobby projects | $20/month Pro |
| **Railway** | $5 credit/month | Pay as you go |
| **Render** | 750 hours/month | $7/month |
| **Heroku** | No free tier | $7/month |

**Recommendation**: Start with Railway (backend) + Vercel (frontend) for best free tier.

---

## 🚨 Troubleshooting

### **Backend won't stay running**
- Ensure platform supports long-running processes
- Check logs for thread errors
- Verify Procfile is correct

### **Frontend can't connect to backend**
- Check CORS configuration
- Verify VITE_API_URL is set correctly
- Check backend is deployed and running

### **Watcher not checking**
- Verify WATCHLOOP_CHECK_INTERVAL is set
- Check backend logs for thread activity
- Ensure production mode (not debug)

---

## 📝 Post-Deployment

After successful deployment:
1. Update repository README with live demo links
2. Test all functionality on production
3. Monitor logs for errors
4. Set up error tracking (Sentry, optional)

---

**Next Steps**: Choose your deployment platform and follow the guide above!
