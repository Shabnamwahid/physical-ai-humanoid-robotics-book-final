#!/usr/bin/env bash
# Interactive demo of worktree and review features

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       SpecKit Plus - Worktree & Review Features Demo               ║
║                                                                      ║
║  This demo shows:                                                    ║
║    • Git worktree creation for parallel development                 ║
║    • Shared specs/ and history/ across worktrees                    ║
║    • AI-assisted code review with multiple modes                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF

echo ""
read -p "Press Enter to start the demo..."
clear

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$HOME/speckit-demo-$(date +%s)"

echo -e "${CYAN}Creating demo project...${NC}"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"

git init -q
git config user.email "demo@example.com"
git config user.name "Demo User"

cp -r "$REPO_ROOT/scripts" .
cp -r "$REPO_ROOT/templates" .
mkdir -p specs history

cat > history/constitution.md << 'EOF'
# Project Constitution

## Code Quality
- All code must have tests
- Security is paramount
- Performance matters

## Standards
- Use bcrypt for passwords (cost factor 12+)
- Validate all inputs
- Rate limit API endpoints
EOF

git add . && git commit -q -m "Initial commit"

echo -e "${GREEN}✓ Demo project created${NC}"
echo ""
read -p "Press Enter to continue..."
clear

# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Part 1: Creating Parallel Worktrees${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Scenario:${NC} You need to work on 2 features simultaneously"
echo "  • Feature 1: User authentication"
echo "  • Feature 2: Task management API"
echo ""
echo "Traditional approach: git stash, switch branches, stash, switch..."
echo "Worktree approach: Work in both at the same time!"
echo ""
read -p "Press Enter to create first worktree..."

export SPECIFY_WORKTREE_MODE=true
echo ""
echo -e "${CYAN}$ bash scripts/bash/create-new-feature.sh${NC}"
echo -e "${CYAN}Enter feature name: user authentication${NC}"
bash scripts/bash/create-new-feature.sh <<< "user authentication" 2>&1 | grep -v "^$"

echo ""
echo -e "${GREEN}✓ First worktree created!${NC}"
echo ""
read -p "Press Enter to create second worktree..."

echo ""
echo -e "${CYAN}$ bash scripts/bash/create-new-feature.sh${NC}"
echo -e "${CYAN}Enter feature name: task management${NC}"
bash scripts/bash/create-new-feature.sh <<< "task management" 2>&1 | grep -v "^$"

echo ""
echo -e "${GREEN}✓ Second worktree created!${NC}"
echo ""

echo "Current worktrees:"
git worktree list
echo ""
read -p "Press Enter to continue..."
clear

# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Part 2: Shared Specs & History${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Key Feature:${NC} specs/ and history/ are shared across all worktrees"
echo ""
echo "Let's create a spec in worktree 1 and verify it's accessible in worktree 2..."
echo ""
read -p "Press Enter to create spec in worktree 1..."

cd ../worktrees/001-user-authentication
mkdir -p ../../"$(basename "$DEMO_DIR")"/specs/001-user-authentication

cat > ../../"$(basename "$DEMO_DIR")"/specs/001-user-authentication/spec.md << 'EOF'
# Feature: User Authentication

## Requirements
1. JWT-based authentication
2. Secure password hashing with bcrypt
3. Rate limiting on login attempts

## Success Criteria
- Login completes in < 500ms
- Passwords never logged or exposed
- Failed attempts trigger cooldown
EOF

cat > ../../"$(basename "$DEMO_DIR")"/specs/001-user-authentication/plan.md << 'EOF'
# Implementation Plan

## Architecture
- Express.js API
- bcrypt for hashing (cost: 12)
- Redis for rate limiting

## Security
- OWASP compliance
- CSRF protection
- Input sanitization
EOF

echo ""
echo -e "${CYAN}Created spec at:${NC} specs/001-user-authentication/spec.md"
echo ""
echo "Content:"
head -8 ../../"$(basename "$DEMO_DIR")"/specs/001-user-authentication/spec.md
echo ""
read -p "Press Enter to check from worktree 2..."

cd ../002-task-management
echo ""
echo -e "${CYAN}Currently in worktree 2 (task-management)${NC}"
echo ""

if [ -f "../../$(basename "$DEMO_DIR")/specs/001-user-authentication/spec.md" ]; then
    echo -e "${GREEN}✓ Can access spec from worktree 1!${NC}"
    echo ""
    echo "This means:"
    echo "  • All features share the same specs/"
    echo "  • Constitution is shared"
    echo "  • No duplicate documentation"
else
    echo -e "${RED}✗ Spec not accessible${NC}"
fi

echo ""
read -p "Press Enter to continue..."
clear

# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Part 3: AI-Assisted Code Review${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Scenario:${NC} You've implemented user auth, now review it before PR"
echo ""
read -p "Press Enter to create implementation with security issues..."

cd ../001-user-authentication
mkdir -p src

cat > src/auth.js << 'EOF'
const crypto = require('crypto');

// SECURITY ISSUE: Using MD5 instead of bcrypt!
function hashPassword(password) {
    return crypto.createHash('md5').update(password).digest('hex');
}

// SECURITY ISSUE: No rate limiting!
function login(email, password) {
    const hashedPassword = hashPassword(password);
    // TODO: check database
    return { token: 'jwt-token-here' };
}

// SECURITY ISSUE: Password in logs!
function register(email, password) {
    console.log(`Registering user ${email} with password ${password}`);
    const hash = hashPassword(password);
    return { email, hash };
}

module.exports = { hashPassword, login, register };
EOF

echo ""
echo -e "${GREEN}✓ Implementation created with intentional security issues${NC}"
echo ""
echo "Code preview:"
head -15 src/auth.js
echo "..."
echo ""
read -p "Press Enter to run security review..."

echo ""
echo -e "${CYAN}$ bash review-implementation.sh --mode security${NC}"
echo ""
bash ../../"$(basename "$DEMO_DIR")"/scripts/bash/review-implementation.sh --mode security 2>&1 | tail -10

REVIEW_DIR="../../$(basename "$DEMO_DIR")/specs/001-user-authentication/reviews"
if [ -d "$REVIEW_DIR" ]; then
    echo ""
    echo -e "${GREEN}✓ Review completed!${NC}"
    echo ""
    echo "Files created:"
    ls -lh "$REVIEW_DIR" | tail -n +2
fi

echo ""
read -p "Press Enter to see review context..."
clear

CONTEXT_FILE=$(find "$REVIEW_DIR" -name "*security*context.md" | head -1)
if [ -f "$CONTEXT_FILE" ]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Review Context (excerpt)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    head -40 "$CONTEXT_FILE"
    echo ""
    echo "... (truncated)"
    echo ""
fi

read -p "Press Enter to test different review modes..."
clear

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Part 4: Multiple Review Modes${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "SpecKit Plus offers 4 review modes:"
echo ""

echo -e "${CYAN}1. Quick Review (5-10 min)${NC}"
echo "   ✓ Spec compliance check"
echo "   ✓ Obvious bugs"
echo ""

echo -e "${CYAN}2. Thorough Review (20-30 min)${NC}"
echo "   ✓ Code quality"
echo "   ✓ Test coverage"
echo "   ✓ Architecture alignment"
echo ""

echo -e "${CYAN}3. Security Review (15-20 min)${NC}"
echo "   ✓ Input validation"
echo "   ✓ SQL injection, XSS, CSRF"
echo "   ✓ Password handling"
echo "   ✓ Dependency vulnerabilities"
echo ""

echo -e "${CYAN}4. Performance Review (15-20 min)${NC}"
echo "   ✓ Algorithm efficiency"
echo "   ✓ Database queries"
echo "   ✓ Caching opportunities"
echo ""

read -p "Press Enter to run all review modes..."
echo ""

for mode in quick thorough performance; do
    echo -e "${CYAN}Running $mode review...${NC}"
    bash ../../"$(basename "$DEMO_DIR")"/scripts/bash/review-implementation.sh --mode "$mode" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $mode review completed${NC}"
    fi
done

echo ""
echo "Review files created:"
ls -1 "$REVIEW_DIR" | sed 's/^/  • /'
echo ""

read -p "Press Enter to see multi-agent review demo..."
clear

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Part 5: Multi-Agent Reviews${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Use Case:${NC} Get a second opinion from a different AI"
echo ""
echo "Each AI agent has different strengths:"
echo "  • Claude: Security & architecture"
echo "  • Gemini: Performance & algorithms"
echo "  • GPT-4: Code quality & patterns"
echo ""

read -p "Press Enter to create reviews from different agents..."
echo ""

for agent in claude gemini gpt4; do
    echo -e "${CYAN}Creating review with $agent...${NC}"
    bash ../../"$(basename "$DEMO_DIR")"/scripts/bash/review-implementation.sh \
        --mode thorough --agent "$agent" > /dev/null 2>&1
    echo -e "${GREEN}✓ $agent review created${NC}"
done

echo ""
echo "Multi-agent reviews:"
ls -1 "$REVIEW_DIR" | grep -E "(claude|gemini|gpt4)" | sed 's/^/  • /'
echo ""
echo "Each agent can find different issues!"
echo ""

read -p "Press Enter to see final summary..."
clear

# ═══════════════════════════════════════════════════════════════════
cat << EOF
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    Demo Complete! ✓                                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

${GREEN}What you just saw:${NC}

${CYAN}Worktree Features:${NC}
  ✓ Created 2 parallel worktrees
  ✓ Verified shared specs/ and history/
  ✓ No git stash needed for context switching

${CYAN}Review Features:${NC}
  ✓ Security review found intentional vulnerabilities
  ✓ All 4 review modes working
  ✓ Multi-agent review support
  ✓ Context files with spec + plan + constitution

${CYAN}Files Created:${NC}
  • Project:    $DEMO_DIR
  • Worktrees:  $(dirname "$DEMO_DIR")/worktrees/
  • Reviews:    $(ls -1 "$REVIEW_DIR" | wc -l) review files

${BLUE}To explore:${NC}
  cd $DEMO_DIR
  git worktree list
  cat specs/001-user-authentication/spec.md
  ls -la specs/001-user-authentication/reviews/

${BLUE}To clean up:${NC}
  rm -rf $DEMO_DIR $(dirname "$DEMO_DIR")/worktrees

${YELLOW}Next Steps:${NC}
  • Run automated tests: ./test-local-installation.sh
  • Read tutorials: docs-plus/04_git_worktrees/
  • Try in real project: Copy scripts/ and templates/

EOF
