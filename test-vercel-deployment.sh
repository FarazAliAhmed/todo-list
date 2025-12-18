#!/bin/bash

echo "🔍 Testing Vercel Deployment Status..."
echo ""

# Test main site
echo "1. Testing main site..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://todo-list-frontend-weld.vercel.app)
if [ "$STATUS" -eq 200 ]; then
    echo "   ✅ Main site is UP (Status: $STATUS)"
else
    echo "   ❌ Main site issue (Status: $STATUS)"
fi
echo ""

# Test debug endpoint
echo "2. Testing debug endpoint..."
DEBUG_RESPONSE=$(curl -s https://todo-list-frontend-weld.vercel.app/api/auth/debug)
echo "   Response: $DEBUG_RESPONSE"
echo ""

# Test if it's the latest deployment (check for our fix)
echo "3. Checking deployment timestamp..."
TIMESTAMP=$(echo $DEBUG_RESPONSE | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
echo "   Last deployment: $TIMESTAMP"
echo ""

# Test backend connection
echo "4. Testing backend API..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://faraz7530-todo-backend.hf.space/docs)
if [ "$BACKEND_STATUS" -eq 200 ]; then
    echo "   ✅ Backend is UP (Status: $BACKEND_STATUS)"
else
    echo "   ❌ Backend issue (Status: $BACKEND_STATUS)"
fi
echo ""

echo "✅ Deployment test complete!"
echo ""
echo "🌐 Frontend URL: https://todo-list-frontend-weld.vercel.app"
echo "🔧 Backend URL: https://faraz7530-todo-backend.hf.space"
echo "📚 API Docs: https://faraz7530-todo-backend.hf.space/docs"
