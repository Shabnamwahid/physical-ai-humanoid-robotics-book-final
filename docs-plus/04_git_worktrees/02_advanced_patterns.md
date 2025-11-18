# Advanced Git Worktree Patterns

## Overview

Master advanced techniques for using git worktrees with SpecKit Plus in real-world scenarios. This guide covers team collaboration, large-scale parallel development, and production deployment patterns.

**Key Learning:**
- Coordinate worktrees across team members
- Handle long-running feature branches
- Integrate worktrees with CI/CD pipelines
- Manage dependencies between parallel features
- Optimize for large teams (5-20 developers)

**Prerequisites:**
- Complete [Multi-Session Workflow Tutorial](01_multi_session_workflow.md)
- Experience with at least 3 parallel worktrees
- Understanding of SpecKit Plus workflow
- Team environment (or simulated multi-user setup)

## Pattern 1: Team Coordination with Worktrees

### Scenario: 5 Developers, 5 Features

**Team Setup:**
- Main repo shared on GitHub
- Each developer works on 2-3 features simultaneously
- Features have dependencies on each other

**Directory Structure (Each Developer):**
```
developer-a/
├── main-repo/           ← Clone of shared repo
│   ├── specs/           ← Shared across team (via git)
│   └── history/         ← Shared across team (via git)
└── worktrees/
    ├── 001-auth/        ← Dev A's features
    └── 002-profile/

developer-b/
├── main-repo/
└── worktrees/
    ├── 003-tasks/       ← Dev B's features
    └── 004-notifications/

developer-c/
├── main-repo/
└── worktrees/
    ├── 005-reports/     ← Dev C's features
    └── 006-export/
```

### Workflow

#### Developer A: Start New Feature

```bash
cd main-repo

# Pull latest specs from team
git pull origin main

# Create feature worktree
/sp.worktree create "user authentication"

cd ../worktrees/001-auth
/sp.specify "OAuth2 authentication with Google, GitHub, and Microsoft"
/sp.plan

# Commit spec to share with team
git add ../../main-repo/specs/001-auth/
git commit -m "spec: Add OAuth2 authentication specification"
git push origin 001-auth
```

#### Developer B: Reference Developer A's Feature

```bash
cd main-repo
git pull origin main  # Gets Dev A's spec updates

# Create dependent feature
/sp.worktree create "task management"

cd ../worktrees/003-tasks
/sp.specify "Task CRUD operations. Requires authentication from 001-auth feature."

# Read Dev A's spec to understand auth system
cat ../../main-repo/specs/001-auth/spec.md

/sp.plan
# AI plans tasks that integrate with 001-auth
```

#### Team Standup: Check All Features

```bash
# Developer A
cd main-repo
git fetch --all

# View all team's features
ls specs/
# 001-auth/         ← Dev A
# 002-profile/      ← Dev A
# 003-tasks/        ← Dev B
# 004-notifications/← Dev B
# 005-reports/      ← Dev C
# 006-export/       ← Dev C

# Check specific feature status
cat specs/003-tasks/spec.md  # See what Dev B is building
```

### Best Practice: Spec-First Collaboration

```bash
# Rule: Always commit specs BEFORE implementing
# This lets teammates see what you're building

# Good workflow:
/sp.specify "My feature"
git commit -am "spec: Add my feature spec"
git push origin 001-my-feature
# ✅ Team can see your plan

/sp.implement
# Now implement (teammates already know what you're doing)

# Bad workflow:
/sp.implement
# ❌ Team doesn't know what you're building until PR
```

## Pattern 2: Long-Running Feature Branches

### Scenario: Feature Takes 2 Weeks, Main Evolves

**Challenge:** Your feature branch `001-big-feature` diverges from main as team commits to main daily.

**Solution: Regular Rebase from Worktree**

```bash
cd worktrees/001-big-feature

# Day 1: Start feature
/sp.specify "Large refactoring of payment system"
/sp.plan

# Day 3: Main has advanced, rebase
git fetch origin main
git rebase origin/main

# Resolve conflicts if any
vim src/payments/processor.ts
git add .
git rebase --continue

# Continue work
/sp.implement

# Day 7: Rebase again
git fetch origin main
git rebase origin/main

# Day 14: Feature complete
git commit -am "feat: Complete payment system refactor"
git push origin 001-big-feature --force-with-lease

# Create PR
gh pr create --title "Refactor: Payment System"
```

**Alternative: Merge Strategy**

```bash
# If rebase is too complex, merge main periodically
cd worktrees/001-big-feature

git fetch origin main
git merge origin/main

# Resolve conflicts
git commit -am "merge: Incorporate latest main changes"
git push origin 001-big-feature
```

## Pattern 3: Hotfix Workflow with Worktrees

### Scenario: Production Bug During Feature Development

```bash
# You're working on Feature A
cd worktrees/001-feature-a
vim src/feature-a.ts
# Uncommitted changes, half-done work

# URGENT: Production bug in payment processing!

# Option 1: Create hotfix worktree from main
cd ../../main-repo
/sp.worktree create "hotfix-payment-crash"

cd ../worktrees/hotfix-payment-crash
# Start from main branch (clean)

# Fix bug quickly
vim src/payments/stripe.ts
npm test
git commit -am "fix: Handle null customer ID in Stripe integration"
git push origin hotfix-payment-crash

# Create emergency PR
gh pr create \
  --title "HOTFIX: Payment crash on null customer" \
  --base main \
  --assignee @me

# Option 2: Use main repo directly (faster for tiny fixes)
cd ../../main-repo
git checkout -b hotfix-payment-crash
# Fix, commit, push, PR

# After hotfix merged
cd worktrees/001-feature-a
# ✅ Your work is still here, untouched!

# Pull hotfix into your feature
git fetch origin main
git merge origin/main
# Continue working
```

## Pattern 4: Experimental Features (Spike Work)

### Scenario: Test 3 Different Approaches

```bash
# Create 3 worktrees to test different solutions
/sp.worktree create "approach-1-rest-api"
/sp.worktree create "approach-2-graphql"
/sp.worktree create "approach-3-grpc"

# Terminal 1: REST API approach
cd worktrees/007-approach-1-rest-api
/sp.specify "RESTful API with OpenAPI spec"
/sp.implement
# Build prototype...
npm run benchmark
# Results: 500 req/s

# Terminal 2: GraphQL approach
cd worktrees/008-approach-2-graphql
/sp.specify "GraphQL API with Apollo Server"
/sp.implement
# Build prototype...
npm run benchmark
# Results: 800 req/s

# Terminal 3: gRPC approach
cd worktrees/009-approach-3-grpc
/sp.specify "gRPC API with Protocol Buffers"
/sp.implement
# Build prototype...
npm run benchmark
# Results: 1200 req/s ← Winner!

# Decision: Use gRPC
cd ../../main-repo

# Keep winner, delete losers
/sp.worktree remove ../worktrees/007-approach-1-rest-api
/sp.worktree remove ../worktrees/008-approach-2-graphql

# Continue with gRPC worktree
cd worktrees/009-approach-3-grpc
# Polish and complete feature
```

## Pattern 5: CI/CD Integration

### Pattern 5a: Test Each Worktree Independently

**.github/workflows/test-feature.yml:**
```yaml
name: Test Feature Branch

on:
  push:
    branches:
      - '[0-9][0-9][0-9]-*'  # Matches 001-feature-name

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Check spec exists
        run: |
          BRANCH_NAME=${GITHUB_REF#refs/heads/}
          SPEC_PATH="specs/${BRANCH_NAME}/spec.md"
          if [ ! -f "$SPEC_PATH" ]; then
            echo "Error: Spec not found at $SPEC_PATH"
            exit 1
          fi
```

### Pattern 5b: Deploy Each Worktree to Preview Environment

```yaml
name: Deploy Preview

on:
  push:
    branches:
      - '[0-9][0-9][0-9]-*'

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Extract feature number
        id: feature
        run: |
          BRANCH=${GITHUB_REF#refs/heads/}
          FEATURE_NUM=${BRANCH%-*}
          echo "number=$FEATURE_NUM" >> $GITHUB_OUTPUT

      - name: Deploy to preview
        run: |
          npm run build
          vercel deploy --name=feature-${{ steps.feature.outputs.number }}

      - name: Comment PR with preview URL
        uses: actions/github-script@v6
        with:
          script: |
            const url = `https://feature-${{ steps.feature.outputs.number }}.vercel.app`
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `🚀 Preview deployed: ${url}`
            })
```

## Pattern 6: Large Team Coordination (10+ Developers)

### Namespace Features by Team

```
specs/
├── team-frontend/
│   ├── 001-ui-components/
│   ├── 002-dashboard/
│   └── 003-mobile-app/
├── team-backend/
│   ├── 011-api-gateway/
│   ├── 012-auth-service/
│   └── 013-data-pipeline/
└── team-infra/
    ├── 021-kubernetes-setup/
    ├── 022-monitoring/
    └── 023-ci-cd/
```

**Create namespaced worktrees:**
```bash
# Frontend team
/sp.worktree create "team-frontend/ui-components"
# → Creates: worktrees/team-frontend-001-ui-components

# Backend team
/sp.worktree create "team-backend/auth-service"
# → Creates: worktrees/team-backend-012-auth-service
```

### Dependency Management

**specs/dependencies.yaml:**
```yaml
features:
  - id: 001-ui-components
    team: frontend
    dependencies: []
    status: in-progress

  - id: 012-auth-service
    team: backend
    dependencies: []
    status: complete

  - id: 002-dashboard
    team: frontend
    dependencies:
      - 012-auth-service  # Requires auth
    status: blocked
    blocked_by: 012-auth-service

  - id: 013-data-pipeline
    team: backend
    dependencies:
      - 012-auth-service  # Requires auth
    status: in-progress
```

## Pattern 7: Stacked Features (Dependent Worktrees)

### Scenario: Feature B Depends on Feature A

```bash
# Feature A: Foundation (must complete first)
/sp.worktree create "user authentication"
cd worktrees/001-auth
/sp.specify "OAuth2 authentication"
/sp.implement
git commit -am "feat: Complete authentication"
git push origin 001-auth

# Feature B: Depends on Feature A
/sp.worktree create "user profiles"
cd worktrees/002-profiles

# Base off Feature A's branch (not main!)
git merge --no-ff 001-auth

/sp.specify "User profile management. Requires 001-auth."
/sp.implement

# Feature B includes Feature A's code
git commit -am "feat: Add user profiles"
git push origin 002-profiles

# Create stacked PR
gh pr create \
  --title "Feature: User Profiles" \
  --base 001-auth \  # ← Base off Feature A!
  --body "Depends on #123 (001-auth)"
```

**Workflow:**
1. Merge Feature A first
2. Update Feature B to base off main
3. Merge Feature B

## Pattern 8: Performance Optimization

### Reduce Worktree Disk Usage

```bash
# Share build artifacts between worktrees
cd worktrees/001-feature-a
ln -s ../../main-repo/node_modules node_modules

cd ../002-feature-b
ln -s ../../main-repo/node_modules node_modules

# Now all worktrees share node_modules
# Install dependencies once in main repo
cd ../../main-repo
npm install

# All worktrees can use these dependencies
```

**Caution:** This works if all features use the same dependencies. For different dependency versions, install separately in each worktree.

### Cleanup Merged Features Automatically

**cleanup-worktrees.sh:**
```bash
#!/bin/bash
# Auto-cleanup merged feature worktrees

# Get list of merged branches
MERGED_BRANCHES=$(git branch --merged main | grep -E '^  [0-9]{3}-' | tr -d ' ')

for branch in $MERGED_BRANCHES; do
  # Find worktree for this branch
  WORKTREE_PATH=$(git worktree list | grep "$branch" | awk '{print $1}')

  if [ -n "$WORKTREE_PATH" ]; then
    echo "Removing merged worktree: $WORKTREE_PATH"
    git worktree remove "$WORKTREE_PATH"
    git branch -d "$branch"
  fi
done

echo "Pruning stale worktree references..."
git worktree prune
```

## Pattern 9: Documentation and Handoff

### Document Worktree Setup for Team

**team-setup.md:**
```markdown
# Team Worktree Setup

## Initial Setup

1. Clone repo:
   ```bash
   git clone https://github.com/team/project.git
   cd project
   ```

2. Enable worktree mode:
   ```bash
   export SPECIFY_WORKTREE_MODE=true
   echo 'export SPECIFY_WORKTREE_MODE=true' >> ~/.bashrc
   ```

3. Create your feature worktrees:
   ```bash
   /sp.worktree create "your-feature-name"
   cd ../worktrees/NNN-your-feature-name
   ```

## Daily Workflow

- **Morning:** Sync specs from team
  ```bash
  cd main-repo && git pull origin main
  ```

- **During work:** Commit specs early
  ```bash
  cd worktrees/NNN-your-feature
  /sp.specify "Your feature"
  git commit -am "spec: Add your feature spec"
  git push origin NNN-your-feature
  ```

- **Before EOD:** Push progress
  ```bash
  git commit -am "wip: Daily progress on feature"
  git push origin NNN-your-feature
  ```

## Tips

- Keep 2-3 worktrees max per developer
- Clean up merged features weekly
- Share specs early, implement later
```

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting Which Worktree You're In

**Solution:**
```bash
# Add to ~/.bashrc
parse_git_worktree() {
  local branch=$(git branch --show-current 2>/dev/null)
  if [ -n "$branch" ]; then
    echo "[$branch]"
  fi
}

export PS1="\$(parse_git_worktree) \$ "

# Now your prompt shows: [001-feature-a] $
```

### Pitfall 2: Worktree and Main Out of Sync

**Solution:** Sync daily

```bash
# Morning routine
cd main-repo
git pull origin main

cd worktrees/001-feature
git merge origin/main  # or rebase
```

### Pitfall 3: Too Many Worktrees

**Symptom:** Confused about what's where

**Solution:** Limit to 3 active worktrees per developer

```bash
# Good
worktrees/
├── 001-critical-feature/
├── 002-experimental/
└── 003-bugfix/

# Bad (too many)
worktrees/
├── 001-feature/
├── 002-feature/
├── 003-feature/
├── 004-feature/
├── 005-feature/  # ❌ Can't keep track!
```

## Success Metrics

After mastering these patterns:

- ✅ Coordinate 5+ parallel features across team
- ✅ Handle long-running branches (2+ weeks)
- ✅ Deploy preview environments per worktree
- ✅ Manage feature dependencies effectively
- ✅ Reduce context-switching time by 80%
- ✅ Maintain clean git history across team

## Related Resources

- [Multi-Session Workflow](01_multi_session_workflow.md)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [SpecKit Plus Test Suite](../../tests/worktree/README.md)

---

**Next Level:** Share your team's worktree patterns! Contribute to [SpecKit Plus Discussions](https://github.com/panaversity/spec-kit-plus/discussions).
