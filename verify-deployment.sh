#!/bin/bash

# Deployment Verification Script
# This script verifies that the Evolution of Todo application is deployed correctly

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

# Print header
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Evolution of Todo - Deployment Verification         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Frontend URL:${NC} $FRONTEND_URL"
echo -e "${YELLOW}Backend URL:${NC} $BACKEND_URL"
echo ""

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Function to check a test
check_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Checking $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

# Frontend checks
echo -e "${BLUE}━━━ Frontend Checks ━━━${NC}"
check_test "Frontend accessibility" "curl -s -o /dev/null -w '%{http_code}' '$FRONTEND_URL' | grep -q '200'"
check_test "Frontend response time" "timeout 5 curl -s '$FRONTEND_URL' > /dev/null"
echo ""

# Backend checks
echo -e "${BLUE}━━━ Backend Checks ━━━${NC}"
check_test "Backend health endpoint" "curl -s '$BACKEND_URL/health' | grep -q 'healthy'"
check_test "Backend API docs" "curl -s -o /dev/null -w '%{http_code}' '$BACKEND_URL/docs' | grep -q '200'"
check_test "Backend root endpoint" "curl -s '$BACKEND_URL/' | grep -q 'Todo API'"
echo ""

# API checks
echo -e "${BLUE}━━━ API Checks ━━━${NC}"
check_test "Health check response format" "curl -s '$BACKEND_URL/health' | grep -q 'status.*healthy'"
check_test "API version in response" "curl -s '$BACKEND_URL/health' | grep -q 'version'"
echo ""

# CORS checks (if backend is accessible)
echo -e "${BLUE}━━━ CORS Checks ━━━${NC}"
check_test "CORS headers present" "curl -s -I -H 'Origin: $FRONTEND_URL' '$BACKEND_URL/health' | grep -qi 'access-control'"
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Summary:${NC}"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✨ All checks passed! Deployment looks good.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some checks failed. Please review the output above.${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting tips:${NC}"
    echo "  1. Ensure both frontend and backend are running"
    echo "  2. Check environment variables are configured correctly"
    echo "  3. Verify CORS_ORIGINS includes the frontend URL"
    echo "  4. Review logs for any errors"
    echo ""
    echo "For more help, see VERIFICATION.md"
    exit 1
fi
