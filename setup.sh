#!/bin/bash

echo "=================================="
echo "Job Search Automation Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}This script will help you set up the job search automation.${NC}"
echo ""

# Step 1: Check if Git is installed
echo -e "${YELLOW}Step 1: Checking Git installation...${NC}"
if ! command -v git &> /dev/null
then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
else
    echo -e "${GREEN}✅ Git is installed${NC}"
fi

# Step 2: Initialize Git repository
echo ""
echo -e "${YELLOW}Step 2: Initializing Git repository...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository already exists${NC}"
fi

# Step 3: Create .gitignore
echo ""
echo -e "${YELLOW}Step 3: Creating .gitignore...${NC}"
cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Excel temporary files
~$*.xlsx

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
GITIGNORE

echo -e "${GREEN}✅ .gitignore created${NC}"

# Step 4: Add all files
echo ""
echo -e "${YELLOW}Step 4: Adding files to Git...${NC}"
git add .
echo -e "${GREEN}✅ Files added${NC}"

# Step 5: Initial commit
echo ""
echo -e "${YELLOW}Step 5: Creating initial commit...${NC}"
git commit -m "Initial commit: Job search automation setup"
echo -e "${GREEN}✅ Initial commit created${NC}"

# Step 6: Instructions for GitHub
echo ""
echo "=================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================="
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Create a new PRIVATE repository on GitHub"
echo "   Visit: https://github.com/new"
echo "   Name: job-search-automation"
echo "   Make it PRIVATE ✓"
echo ""
echo "2. Connect this folder to your GitHub repository:"
echo "   Run these commands:"
echo ""
echo -e "${YELLOW}   git remote add origin https://github.com/YOUR-USERNAME/job-search-automation.git${NC}"
echo -e "${YELLOW}   git branch -M main${NC}"
echo -e "${YELLOW}   git push -u origin main${NC}"
echo ""
echo "3. Enable GitHub Actions:"
echo "   - Go to your repo Settings → Actions → General"
echo "   - Set Workflow permissions to 'Read and write permissions'"
echo "   - Save"
echo ""
echo "4. The automation will run every 6 hours automatically!"
echo "   Or trigger manually from Actions tab"
echo ""
echo "=================================="
echo -e "${GREEN}Questions? Check README.md for full documentation${NC}"
echo "=================================="
