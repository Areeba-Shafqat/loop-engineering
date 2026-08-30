#!/bin/bash

# Update Frontend with Railway Backend URL
# Usage: ./connect-backend.sh <your-railway-backend-url>

if [ -z "$1" ]; then
    echo "❌ Error: Please provide the Railway backend URL"
    echo ""
    echo "Usage: ./connect-backend.sh https://your-backend-url.railway.app"
    echo ""
    echo "To get your backend URL:"
    echo "1. Open: https://railway.com/project/ad7cbc23-7fc4-4159-b3ff-147d8330e01b"
    echo "2. Click on 'loop-engineering' service"
    echo "3. Go to Settings → Networking"
    echo "4. Click 'Generate Domain' if not generated"
    echo "5. Copy the public URL"
    exit 1
fi

BACKEND_URL=$1

# Remove trailing slash if present
BACKEND_URL=${BACKEND_URL%/}

echo "=================================================="
echo "  Connecting Frontend to Backend"
echo "=================================================="
echo ""
echo "Backend URL: $BACKEND_URL"
echo "Frontend: https://frontend-fawn-six-17.vercel.app"
echo ""

# Test backend health
echo "🔍 Testing backend health..."
HEALTH_CHECK=$(curl -s "$BACKEND_URL/api/health" | grep -o '"success":true' || echo "")

if [ -z "$HEALTH_CHECK" ]; then
    echo "⚠️  Warning: Backend health check failed"
    echo "   URL: $BACKEND_URL/api/health"
    echo "   The backend might still be deploying or there's an issue"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Backend is healthy!"
fi

echo ""
echo "🚀 Updating Vercel frontend environment variable..."

cd "$(dirname "$0")/frontend"

# Set environment variable in Vercel
vercel env rm VITE_API_URL production -y 2>/dev/null || true
echo "$BACKEND_URL/api" | vercel env add VITE_API_URL production

echo ""
echo "🔄 Redeploying frontend..."
vercel --prod

echo ""
echo "=================================================="
echo "✅ Deployment Complete!"
echo "=================================================="
echo ""
echo "Frontend: https://frontend-fawn-six-17.vercel.app"
echo "Backend:  $BACKEND_URL"
echo ""
echo "Test your deployment:"
echo "1. Visit: https://frontend-fawn-six-17.vercel.app"
echo "2. Click 'Start New Task'"
echo "3. Watch it complete!"
echo ""
