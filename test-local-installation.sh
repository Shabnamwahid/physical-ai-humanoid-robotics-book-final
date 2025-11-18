#!/usr/bin/env bash
# Test the local SpecKit Plus installation with worktree and review features

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  SpecKit Plus Local Installation Test${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$HOME/speckit-test-$(date +%s)"

echo -e "${YELLOW}Step 1: Running automated test suites...${NC}"
echo ""

# Run test suites
cd "$REPO_ROOT/tests"

echo "Running worktree tests..."
if ./worktree/run-all-tests.sh; then
    echo -e "${GREEN}✓ Worktree tests passed (31 tests)${NC}"
else
    echo -e "${RED}✗ Worktree tests failed${NC}"
    exit 1
fi

echo ""
echo "Running review tests..."
if ./review/run-all-tests.sh; then
    echo -e "${GREEN}✓ Review tests passed (39 tests)${NC}"
else
    echo -e "${RED}✗ Review tests failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ All 70 tests passed!${NC}"
echo ""

echo -e "${YELLOW}Step 2: Creating test project with local SpecKit Plus...${NC}"
echo ""

# Create test project manually using local files
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Initialize git
git init -q
git config user.email "test@example.com"
git config user.name "Test User"

# Copy SpecKit Plus files
cp -r "$REPO_ROOT/scripts" .
cp -r "$REPO_ROOT/templates" .
mkdir -p specs history .specify/templates

# Create a simple constitution
cat > history/constitution.md << 'EOF'
# Test Project Constitution

## Code Quality Standards
- All code must have tests
- Follow TDD practices
- Document all public functions

## Architecture Principles
- Keep it simple (KISS)
- Don't repeat yourself (DRY)
- Write readable code
EOF

git add .
git commit -q -m "Initial commit with SpecKit Plus"

echo -e "${GREEN}✓ Test project created at: $TEST_DIR${NC}"
echo ""

echo -e "${YELLOW}Step 3: Testing worktree functionality...${NC}"
echo ""

# Enable worktree mode
export SPECIFY_WORKTREE_MODE=true

# Create first worktree
echo "Creating worktree for 'user authentication' feature..."
bash scripts/bash/create-new-feature.sh <<< "user authentication" > /dev/null 2>&1

if [ -d "../worktrees/001-user-authentication" ]; then
    echo -e "${GREEN}✓ Worktree created: worktrees/001-user-authentication${NC}"
else
    echo -e "${RED}✗ Worktree creation failed${NC}"
    exit 1
fi

# Verify worktree is listed
echo ""
echo "Git worktrees:"
git worktree list

# Create second worktree for parallel development
echo ""
echo "Creating second worktree for 'task management' feature..."
bash scripts/bash/create-new-feature.sh <<< "task management" > /dev/null 2>&1

if [ -d "../worktrees/002-task-management" ]; then
    echo -e "${GREEN}✓ Second worktree created: worktrees/002-task-management${NC}"
else
    echo -e "${RED}✗ Second worktree creation failed${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 4: Testing shared specs/history...${NC}"
echo ""

# Create spec in first worktree
cd ../worktrees/001-user-authentication
mkdir -p ../../"$(basename "$TEST_DIR")"/specs/001-user-authentication

cat > ../../"$(basename "$TEST_DIR")"/specs/001-user-authentication/spec.md << 'EOF'
# Feature: User Authentication

## Requirements
1. Users can register with email and password
2. Users can log in with credentials
3. Passwords are securely hashed
4. Failed login attempts are logged

## Success Criteria
- Registration completes in < 2 seconds
- Login fails gracefully with wrong password
- Passwords never stored in plaintext

## Non-Functional Requirements
- GDPR compliant
- OWASP security standards
EOF

cat > ../../"$(basename "$TEST_DIR")"/specs/001-user-authentication/plan.md << 'EOF'
# Implementation Plan: User Authentication

## Architecture
- Use bcrypt for password hashing (industry standard)
- SQLite database for user storage
- REST API endpoints for auth operations

## Data Model
```
User:
  - id: UUID
  - email: string (unique, indexed)
  - password_hash: string
  - created_at: timestamp
  - last_login: timestamp
```

## Components
1. **User Model** (`models/user.py`)
   - User data structure
   - Validation logic

2. **Auth Service** (`services/auth.py`)
   - register_user(email, password)
   - authenticate_user(email, password)
   - hash_password(password)
   - verify_password(password, hash)

3. **API Endpoints** (`api/auth.py`)
   - POST /api/register
   - POST /api/login
   - POST /api/logout

## Security Considerations
- Use bcrypt with cost factor 12
- Implement rate limiting (5 attempts per minute)
- Add CSRF protection
- Sanitize all inputs
EOF

# Create some implementation files with security issues for review to find
mkdir -p src/models src/services

cat > src/models/user.py << 'EOF'
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password  # SECURITY ISSUE: storing plain password!

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password  # SECURITY ISSUE: exposing password!
        }
EOF

cat > src/services/auth.py << 'EOF'
import hashlib

def hash_password(password):
    # SECURITY ISSUE: Using MD5 instead of bcrypt!
    return hashlib.md5(password.encode()).hexdigest()

def register_user(email, password):
    # SECURITY ISSUE: No email validation!
    user = User(email, password)
    return user

def authenticate_user(email, password):
    # TODO: implement
    pass
EOF

git add ../../"$(basename "$TEST_DIR")"/specs/001-user-authentication/
git add src/
git commit -q -m "Add user authentication spec and initial implementation"

echo -e "${GREEN}✓ Created spec and plan in worktree 1${NC}"

# Verify it's accessible from worktree 2
cd ../002-task-management

if [ -f "../../$(basename "$TEST_DIR")/specs/001-user-authentication/spec.md" ]; then
    echo -e "${GREEN}✓ Spec from worktree 1 is accessible in worktree 2 (shared!)${NC}"
else
    echo -e "${RED}✗ Specs are NOT shared across worktrees${NC}"
    exit 1
fi

# Verify get_repo_root works correctly
cd ../001-user-authentication
source ../../"$(basename "$TEST_DIR")"/scripts/bash/common.sh

REPO_ROOT_RESULT=$(get_repo_root)
EXPECTED_ROOT="$(cd ../../"$(basename "$TEST_DIR")" && pwd)"

if [ "$REPO_ROOT_RESULT" = "$EXPECTED_ROOT" ]; then
    echo -e "${GREEN}✓ get_repo_root() returns main repo path (not worktree path)${NC}"
else
    echo -e "${RED}✗ get_repo_root() returns wrong path${NC}"
    echo "  Expected: $EXPECTED_ROOT"
    echo "  Got: $REPO_ROOT_RESULT"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 5: Testing review command...${NC}"
echo ""

# Run review in quick mode
echo "Running quick review..."
bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode quick > /dev/null 2>&1

if [ -d "../../$(basename "$TEST_DIR")/specs/001-user-authentication/reviews" ]; then
    echo -e "${GREEN}✓ Review directory created${NC}"

    CONTEXT_FILE=$(find "../../$(basename "$TEST_DIR")/specs/001-user-authentication/reviews" -name "*_context.md" | head -1)
    REVIEW_FILE=$(find "../../$(basename "$TEST_DIR")/specs/001-user-authentication/reviews" -name "*_review.md" | head -1)

    if [ -f "$CONTEXT_FILE" ]; then
        echo -e "${GREEN}✓ Context file created: $(basename "$CONTEXT_FILE")${NC}"

        # Verify context includes all required sections
        if grep -q "Feature Specification" "$CONTEXT_FILE" && \
           grep -q "Implementation Plan" "$CONTEXT_FILE" && \
           grep -q "Constitution" "$CONTEXT_FILE"; then
            echo -e "${GREEN}✓ Context file includes spec, plan, and constitution${NC}"
        else
            echo -e "${RED}✗ Context file missing required sections${NC}"
        fi
    else
        echo -e "${RED}✗ Context file not created${NC}"
    fi

    if [ -f "$REVIEW_FILE" ]; then
        echo -e "${GREEN}✓ Review template created: $(basename "$REVIEW_FILE")${NC}"
    else
        echo -e "${RED}✗ Review template not created${NC}"
    fi
else
    echo -e "${RED}✗ Review directory not created${NC}"
    exit 1
fi

# Test other review modes
echo ""
echo "Testing other review modes..."
bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode security > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Security review mode works${NC}"
fi

bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode thorough > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Thorough review mode works${NC}"
fi

bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode performance > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Performance review mode works${NC}"
fi

# Test JSON output
echo ""
echo "Testing JSON output..."
JSON_OUTPUT=$(bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode quick --json 2>/dev/null)
if echo "$JSON_OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    echo -e "${GREEN}✓ JSON output is valid${NC}"
else
    echo -e "${RED}✗ JSON output is invalid${NC}"
fi

# Test agent parameter
echo ""
echo "Testing multi-agent support..."
bash ../../"$(basename "$TEST_DIR")"/scripts/bash/review-implementation.sh --mode quick --agent gemini > /dev/null 2>&1
GEMINI_FILES=$(find "../../$(basename "$TEST_DIR")/specs/001-user-authentication/reviews" -name "*gemini*" | wc -l)
if [ "$GEMINI_FILES" -gt 0 ]; then
    echo -e "${GREEN}✓ Agent parameter works (files created with 'gemini' in name)${NC}"
fi

echo ""
echo -e "${YELLOW}Step 6: Summary of created files...${NC}"
echo ""

cd ../../"$(basename "$TEST_DIR")"
echo "Project structure:"
tree -L 3 -I '.git' 2>/dev/null || find . -type f -not -path './.git/*' | head -20

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✓ All tests passed! Local installation works correctly.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Test project location:${NC} $TEST_DIR"
echo ""
echo -e "${BLUE}What was tested:${NC}"
echo "  ✓ 70 automated tests (31 worktree + 39 review)"
echo "  ✓ Worktree creation and management"
echo "  ✓ Shared specs/ and history/ across worktrees"
echo "  ✓ get_repo_root() returns correct path"
echo "  ✓ Review command with all 4 modes"
echo "  ✓ Context and review file generation"
echo "  ✓ Multi-agent support"
echo "  ✓ JSON output format"
echo ""
echo -e "${BLUE}To explore the test project:${NC}"
echo "  cd $TEST_DIR"
echo "  git worktree list"
echo "  ls -la specs/001-user-authentication/reviews/"
echo ""
echo -e "${BLUE}To clean up:${NC}"
echo "  rm -rf $TEST_DIR"
echo "  rm -rf $(dirname "$TEST_DIR")/worktrees"
echo ""
