#!/bin/bash

echo "🚀 Video Quality Checker - Deployment Helper"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}This script will help you deploy your application to Vercel and Render${NC}"
echo ""

# Check if git repo is clean
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: You have uncommitted changes. Consider committing them first.${NC}"
    echo ""
fi

echo -e "${GREEN}Step 1: Backend Deployment on Render${NC}"
echo "1. Go to https://dashboard.render.com/"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect GitHub repo: jerald6111/Video-Quality-Checker"
echo "4. Configure:"
echo "   - Name: video-quality-checker-api"
echo "   - Root Directory: backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python app_production.py"
echo "   - Environment Variables:"
echo "     PORT=5000"
echo "     FLASK_ENV=production"
echo ""

read -p "Press Enter when backend is deployed and note your Render URL..."

echo ""
echo -e "${GREEN}Step 2: Frontend Deployment on Vercel${NC}"
echo "1. Go to https://vercel.com/dashboard"
echo "2. Click 'New Project'"
echo "3. Import repo: jerald6111/Video-Quality-Checker"
echo "4. Configure:"
echo "   - Framework: Create React App"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: build"
echo ""

echo -e "${YELLOW}Enter your Render backend URL (e.g., https://your-app.onrender.com):${NC}"
read -r RENDER_URL

if [ -n "$RENDER_URL" ]; then
    echo ""
    echo -e "${BLUE}Add this environment variable in Vercel:${NC}"
    echo "REACT_APP_API_URL=$RENDER_URL"
    echo ""
fi

echo -e "${GREEN}Step 3: Update CORS Configuration${NC}"
echo "After deploying to Vercel, you'll get a URL like: https://your-app.vercel.app"
echo "Add this URL to the CORS configuration in backend/app_production.py"
echo ""

echo -e "${YELLOW}Would you like to commit the new deployment files? (y/n)${NC}"
read -r commit_choice

if [ "$commit_choice" = "y" ] || [ "$commit_choice" = "Y" ]; then
    git add .
    git commit -m "Add deployment configuration for Vercel and Render

- Added production Flask app with enhanced mock responses
- Created Vercel configuration for frontend deployment  
- Added comprehensive deployment documentation
- Updated CORS settings for production"
    
    echo -e "${GREEN}Committed deployment files!${NC}"
    
    echo -e "${YELLOW}Push to GitHub? (y/n)${NC}"
    read -r push_choice
    
    if [ "$push_choice" = "y" ] || [ "$push_choice" = "Y" ]; then
        git push origin main
        echo -e "${GREEN}Pushed to GitHub!${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 Deployment setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Deploy backend on Render using the instructions above"
echo "2. Deploy frontend on Vercel using the instructions above"
echo "3. Update CORS settings with your actual Vercel URL"
echo "4. Test both services"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "- Full deployment guide: DEPLOYMENT.md"
echo "- Development setup: DEVELOPMENT.md"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
