# Deployment Guide

## 🚀 Deploying to Vercel (Frontend) and Render (Backend)

This guide walks you through deploying the Video Quality Checker application with the frontend on Vercel and backend on Render.

## 📋 Prerequisites

- GitHub repository (✅ already set up)
- Vercel account (free tier available)
- Render account (free tier available)

## 🔧 Backend Deployment on Render

### Step 1: Create Render Web Service

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**: `jerald6111/Video-Quality-Checker`
4. **Configure the service**:

```
Name: video-quality-checker-api
Environment: Docker
Region: Choose your preferred region
Branch: main
```

### Step 2: Configure Build Settings

```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python app_production.py
```

### Step 3: Environment Variables

Add these environment variables in Render:

```
PORT=5000
FLASK_ENV=production
UPLOAD_FOLDER=./temp_videos
MAX_CONTENT_LENGTH=1073741824
```

### Step 4: Deploy

- Click **"Create Web Service"**
- Wait for deployment (usually 2-5 minutes)
- Note your Render URL: `https://your-app-name.onrender.com`

## 🌐 Frontend Deployment on Vercel

### Step 1: Install Vercel CLI (Optional)

```bash
npm i -g vercel
```

### Step 2: Deploy via GitHub Integration

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. **Click "New Project"**
3. **Import your repository**: `jerald6111/Video-Quality-Checker`
4. **Configure project**:

```
Framework Preset: Create React App
Root Directory: frontend
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

### Step 3: Environment Variables

Add this environment variable in Vercel:

```
REACT_APP_API_URL=https://your-render-app.onrender.com
```

**Replace `your-render-app` with your actual Render service name.**

### Step 4: Deploy

- Click **"Deploy"**
- Wait for build completion (usually 1-2 minutes)
- Note your Vercel URL: `https://your-app.vercel.app`

## 🔄 Update CORS Configuration

After getting your Vercel URL, update the backend CORS settings:

1. **Edit `backend/app_production.py`**
2. **Update the CORS origins**:

```python
CORS(app, origins=[
    "https://your-actual-vercel-app.vercel.app",  # Your actual Vercel URL
    "http://localhost:3000"  # Keep for development
])
```

3. **Commit and push changes**:

```bash
git add .
git commit -m "Update CORS for production deployment"
git push origin main
```

Render will automatically redeploy with the updated CORS settings.

## ✅ Verification Steps

### Test Backend (Render)
```bash
# Test health endpoint
curl https://your-render-app.onrender.com/api/health

# Test quality check endpoint
curl -X POST https://your-render-app.onrender.com/api/check_quality \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/test-video", "vocabulary": []}'
```

### Test Frontend (Vercel)
1. Visit your Vercel URL
2. Try submitting a test URL
3. Verify API calls work correctly

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure Vercel URL is added to CORS origins in backend
   - Check that API URL is correct in Vercel environment variables

2. **Build Failures**
   - Check build logs in Render/Vercel dashboards
   - Verify all dependencies are listed in requirements.txt/package.json

3. **API Not Responding**
   - Check Render service logs
   - Verify environment variables are set correctly
   - Ensure Render service is not sleeping (free tier limitation)

### Performance Notes

- **Render Free Tier**: Service may sleep after 15 minutes of inactivity
- **Cold Starts**: First request after sleep may take 30+ seconds
- **Vercel**: Frontend will be fast and always available

## 🚀 Going to Production

For production use with full video processing:

1. **Upgrade Render Plan**: For faster performance and no sleeping
2. **Add System Dependencies**: FFmpeg, Tesseract, OpenCV
3. **File Storage**: Use external storage (AWS S3, Cloudinary) for video files
4. **Monitoring**: Set up logging and error tracking
5. **Custom Domain**: Add your own domain to both services

## 📊 Expected Costs

- **Development/Testing**: Free on both platforms
- **Light Production**: ~$7-25/month (Render Starter + Vercel Pro)
- **Full Production**: $25-100+/month depending on usage

## 🔄 Continuous Deployment

Both platforms will automatically redeploy when you push to the `main` branch, making updates seamless.
