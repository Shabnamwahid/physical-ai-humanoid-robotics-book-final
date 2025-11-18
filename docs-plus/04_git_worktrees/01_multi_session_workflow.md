# Multi-Session Parallel Development with Git Worktrees

## Overview

Learn how to work on multiple features simultaneously across different AI sessions using git worktrees. This workflow is perfect for when you need to juggle multiple priorities, test different approaches in parallel, or collaborate with an AI agent across multiple terminal sessions.

**Key Learning:**
- Work on 2-3 features simultaneously without branch switching
- Resume work on any feature in seconds (no stashing, no context loss)
- Keep main branch always clean and deployable
- Share specs and history across all features automatically

**What you'll accomplish:**
- Set up 3 parallel feature worktrees
- Develop features independently in separate sessions
- Experience the power of context preservation
- Learn best practices for multi-session AI collaboration

## Prerequisites

- SpecKit Plus installed with worktree support
- Git 2.15+ (check with `git --version`)
- Basic understanding of SpecKit Plus workflow ([Quickstart](../05_quickstart/readme.md))
- Multiple terminal windows/tabs (or tmux)

## The Problem This Solves

### Traditional Single-Branch Workflow Pain Points

**Scenario:** You're working on Feature A when an urgent Feature B request comes in.

**Without Worktrees:**
```bash
# Working on Feature A
git checkout 001-feature-a
vim src/feature-a.ts
# ❌ Oh no! Need to switch to Feature B urgently

git stash push -m "WIP: feature A half done"
git checkout 002-feature-b
# Work on Feature B...
git commit -am "Feature B done"

git checkout 001-feature-a
git stash pop
# ❌ Conflicts! What was I doing again?
```

**With Worktrees:**
```bash
# Working on Feature A in Terminal 1
cd worktrees/001-feature-a
vim src/feature-a.ts
# ✅ Leave it as-is!

# Switch to Feature B in Terminal 2
cd worktrees/002-feature-b
vim src/feature-b.ts
# ✅ Work independently!

# Back to Feature A in Terminal 1
# ✅ Everything exactly as you left it!
```

## Tutorial: Build 3 Features in Parallel

We'll build a task management system with 3 features developed simultaneously:
1. **User Authentication** (001-auth)
2. **Task CRUD Operations** (002-tasks)
3. **Task Assignment & Collaboration** (003-collaborate)

### Part 1: Setup - Enable Worktree Mode

#### Step 1: Verify You're in Main Repo

```bash
# Check current location
pwd
# Should be in your main repo

# Verify clean state
git status
# Should show: On branch main, nothing to commit
```

#### Step 2: Enable Worktree Mode (Optional)

**Option A: Per-Session (Recommended for learning)**
```bash
export SPECIFY_WORKTREE_MODE=true
```

**Option B: Permanent**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export SPECIFY_WORKTREE_MODE=true' >> ~/.bashrc
source ~/.bashrc
```

**Note:** With worktree mode enabled, `/sp.specify` automatically creates worktrees. Without it, you create worktrees manually with `/sp.worktree create`.

### Part 2: Create Feature Worktrees

We'll create 3 worktrees, one for each feature.

#### Feature 1: Authentication

```bash
# In main repo
/sp.worktree create "user authentication system"

# Output:
# ✓ Worktree created: /path/to/worktrees/001-user-auth
# Branch: 001-user-auth
#
# To switch to this worktree:
#   cd ../worktrees/001-user-auth
```

**What happened:**
- Created branch `001-user-auth`
- Created worktree at `../worktrees/001-user-auth`
- Main repo still on `main` branch ✅

#### Feature 2: Task CRUD

```bash
# Still in main repo
/sp.worktree create "task CRUD operations"

# Output:
# ✓ Worktree created: /path/to/worktrees/002-task-crud
# Branch: 002-task-crud
```

#### Feature 3: Collaboration

```bash
# Still in main repo
/sp.worktree create "task assignment and collaboration features"

# Output:
# ✓ Worktree created: /path/to/worktrees/003-collaborate
# Branch: 003-collaborate
```

#### Verify Your Setup

```bash
# List all worktrees
/sp.worktree list

# Output:
# /path/to/main-repo                    (main)
# /path/to/worktrees/001-user-auth      (001-user-auth)
# /path/to/worktrees/002-task-crud      (002-task-crud)
# /path/to/worktrees/003-collaborate    (003-collaborate)
```

**Directory Structure Created:**
```
my-project/              ← Main repo (stays on main)
├── specs/               ← Shared across all worktrees
├── history/             ← Shared across all worktrees
└── .git/

worktrees/               ← Feature worktrees
├── 001-user-auth/       ← Feature 1
├── 002-task-crud/       ← Feature 2
└── 003-collaborate/     ← Feature 3
```

### Part 3: Multi-Session Development

Now comes the magic! Open 3 terminal windows/tabs.

#### Terminal 1: Feature 1 (Authentication)

```bash
cd worktrees/001-user-auth

# Create specification
/sp.specify "User authentication system with JWT tokens and refresh tokens. Support email/password login, registration, password reset, and session management."

# AI creates: main-repo/specs/001-user-auth/spec.md

# Review spec
cat ../../main-repo/specs/001-user-auth/spec.md

# Create plan
/sp.plan

# AI creates: main-repo/specs/001-user-auth/plan.md

# Create tasks
/sp.tasks

# AI creates: main-repo/specs/001-user-auth/tasks.md

# Start implementing
/sp.implement

# Work on implementation...
vim src/auth/jwt.ts
vim src/auth/middleware.ts
```

**Leave Terminal 1 running with uncommitted changes!**

#### Terminal 2: Feature 2 (Task CRUD)

```bash
cd worktrees/002-task-crud

# Create specification
/sp.specify "Task CRUD operations. Users can create, read, update, and delete tasks. Tasks have title, description, status, priority, and due date."

# AI creates: main-repo/specs/002-task-crud/spec.md

# Create plan
/sp.plan

# AI creates: main-repo/specs/002-task-crud/plan.md

# Create tasks
/sp.tasks

# Start implementing
/sp.implement

# Work on implementation...
vim src/tasks/service.ts
vim src/tasks/repository.ts
```

**Leave Terminal 2 running with uncommitted changes!**

#### Terminal 3: Feature 3 (Collaboration)

```bash
cd worktrees/003-collaborate

# Create specification
/sp.specify "Task assignment and collaboration. Users can assign tasks to team members, comment on tasks, and receive notifications for task updates."

# AI creates: main-repo/specs/003-collaborate/spec.md

# Create plan
/sp.plan

# Start implementing
/sp.implement

# Work on implementation...
vim src/collaboration/assignments.ts
```

**All 3 terminals have independent working states!**

### Part 4: Context Switching Without Stashing

This is where worktrees shine!

#### Scenario: Urgent Bug in Feature 1

```bash
# In Terminal 1 (Feature 1)
# You have uncommitted changes in auth files
git status
# On branch 001-user-auth
# Changes not staged for commit:
#   modified:   src/auth/jwt.ts
#   modified:   src/auth/middleware.ts

# Boss: "Authentication is broken in production!"
# You: "No problem, I'm already in the auth worktree"

# Fix the bug immediately (no stashing!)
vim src/auth/jwt.ts

# Test
npm test

# Commit
git commit -am "fix: Handle expired JWT tokens correctly"
git push origin 001-user-auth

# Create PR
gh pr create --title "Fix JWT token expiration handling"

# ✅ Bug fixed! Your previous WIP changes are still there
```

#### Switch to Feature 2 Progress

```bash
# In Terminal 2 (Feature 2)
# Check what you were doing
git status
# On branch 002-task-crud
# Your changes from earlier are still here!

# Continue where you left off
vim src/tasks/service.ts

# Run tests
npm test -- --watch

# ✅ No context switching overhead!
```

#### Review All Features at Once

```bash
# Open VS Code with all 3 worktrees
code worktrees/001-user-auth
code worktrees/002-task-crud
code worktrees/003-collaborate

# Or use workspaces
code workspace.code-workspace
```

**workspace.code-workspace:**
```json
{
  "folders": [
    { "path": "worktrees/001-user-auth" },
    { "path": "worktrees/002-task-crud" },
    { "path": "worktrees/003-collaborate" }
  ]
}
```

### Part 5: Shared Specs and History

**The Key Benefit:** All worktrees share the same specs and history!

#### Verify Shared Access

```bash
# In Terminal 1 (Feature 1 worktree)
ls ../../main-repo/specs/
# 001-user-auth/
# 002-task-crud/
# 003-collaborate/

# Create a PHR in Feature 1
/sp.phr --title "Implemented JWT auth" --stage green

# AI creates: main-repo/history/prompts/001-user-auth/0001-implemented-jwt-auth.green.prompt.md
```

```bash
# In Terminal 2 (Feature 2 worktree)
ls ../../main-repo/history/prompts/
# 001-user-auth/   ← Can see Feature 1's history!
# 002-task-crud/   ← Your own history
# 003-collaborate/ ← Can see Feature 3's history!

# All history is visible from any worktree ✅
```

#### Cross-Reference Features

```bash
# In Feature 3 spec, reference Feature 1
cd worktrees/003-collaborate
vim ../../main-repo/specs/003-collaborate/spec.md

# Add to spec:
# ## Dependencies
# - Requires authentication system from 001-user-auth
# - See `specs/001-user-auth/spec.md` for auth details

# The spec file is in the main repo, visible to all worktrees!
```

### Part 6: Best Practices for Multi-Session Work

#### Practice 1: One Worktree Per Feature

✅ **Good:**
```
worktrees/
├── 001-user-auth/
├── 002-task-crud/
└── 003-notifications/
```

❌ **Avoid:**
```
worktrees/
└── all-features-combined/  # Don't do this!
```

#### Practice 2: Regular Commits Per Worktree

```bash
# In each worktree, commit frequently
cd worktrees/001-user-auth
git commit -am "feat: Add JWT token generation"
git push origin 001-user-auth

cd ../002-task-crud
git commit -am "feat: Implement task creation endpoint"
git push origin 002-task-crud
```

#### Practice 3: Keep Main Clean

```bash
# Never work directly in main repo when using worktrees
cd main-repo
git status
# Should always show: On branch main, nothing to commit

# All work happens in worktrees ✅
```

#### Practice 4: Document Feature Dependencies

**In `specs/000-architecture/feature-map.md`:**
```markdown
# Feature Dependency Map

001-user-auth (Foundation)
└── 002-task-crud (Depends on auth)
    └── 003-collaborate (Depends on tasks + auth)
```

### Part 7: Completing and Cleaning Up Features

#### Scenario: Feature 1 Complete

```bash
# In Terminal 1
cd worktrees/001-user-auth

# Final commit
git commit -am "feat: Complete authentication system"
git push origin 001-user-auth

# Create PR
gh pr create \
  --title "Feature: User Authentication System" \
  --body "Implements JWT-based authentication with refresh tokens"

# PR merged! Now clean up
cd ../../main-repo
git pull origin main

# Remove worktree
/sp.worktree remove ../worktrees/001-user-auth

# Delete local branch (merged remotely)
git branch -d 001-user-auth

# Verify
/sp.worktree list
# /path/to/main-repo           (main)
# /path/to/worktrees/002-task-crud    (002-task-crud)
# /path/to/worktrees/003-collaborate  (003-collaborate)
```

**Important:** The spec remains in `specs/001-user-auth/` for historical record! ✅

#### Continue with Remaining Features

```bash
# Features 2 and 3 continue independently
# Terminal 2 and 3 are unaffected by Feature 1 cleanup
```

## Advanced Patterns

### Pattern 1: Hot-Swapping Between Features

```bash
# Define shell functions for quick switching
cat >> ~/.bashrc << 'EOF'
alias wt1='cd /path/to/worktrees/001-user-auth'
alias wt2='cd /path/to/worktrees/002-task-crud'
alias wt3='cd /path/to/worktrees/003-collaborate'
alias wtmain='cd /path/to/main-repo'
EOF

source ~/.bashrc

# Now switch instantly:
wt1  # Jump to Feature 1
wt2  # Jump to Feature 2
wtmain  # Jump to main repo
```

### Pattern 2: Parallel Testing

```bash
# Terminal 1: Test Feature 1
cd worktrees/001-user-auth
npm test -- --watch

# Terminal 2: Test Feature 2
cd worktrees/002-task-crud
npm test -- --watch

# Terminal 3: Test Feature 3
cd worktrees/003-collaborate
npm test -- --watch

# All tests run simultaneously! ✅
```

### Pattern 3: AI Session Per Worktree

**Powerful Technique:** Run a separate AI agent session in each worktree!

**Terminal 1:**
```bash
cd worktrees/001-user-auth
claude  # Start Claude AI session

# AI context: "I'm working on authentication in 001-user-auth"
# AI has full context of this feature
```

**Terminal 2:**
```bash
cd worktrees/002-task-crud
claude  # Separate Claude AI session

# AI context: "I'm working on task CRUD in 002-task-crud"
# Different context, no confusion!
```

**Benefits:**
- Each AI session focused on one feature
- No context switching for AI
- AI suggestions more relevant
- Faster iteration per feature

### Pattern 4: Progressive Enhancement

```bash
# Start with core features
/sp.worktree create "core user features"
/sp.worktree create "core task features"

# Later add enhancements
/sp.worktree create "user profile enhancements"
/sp.worktree create "task filtering and search"

# All developed in parallel without blocking each other
```

## Troubleshooting

### Problem: "I forgot which worktree I'm in"

**Solution:**
```bash
# Show current branch in prompt
git branch --show-current
# → 001-user-auth

# Or list all worktrees with current marked
/sp.worktree list
```

### Problem: "I accidentally committed to wrong worktree"

**Solution:**
```bash
# Check where you are
pwd
# /path/to/worktrees/002-task-crud

# Check last commit
git log -1

# If wrong worktree, create patch and apply to correct one
git format-patch -1 HEAD
git reset --hard HEAD~1

# Switch to correct worktree
cd ../001-user-auth
git apply /path/to/patch
```

### Problem: "Specs directory not shared"

**Solution:**
```bash
# Verify you're in a worktree
cd worktrees/001-user-auth
source ../../main-repo/scripts/bash/common.sh
is_worktree && echo "YES" || echo "NO"
# Should output: YES

# Check where specs are accessed from
get_repo_root
# Should output: /path/to/main-repo (NOT worktree path!)

# If incorrect, update SpecKit Plus:
cd ../../main-repo
git pull origin main
```

### Problem: "Too many worktrees, confused"

**Recommendation:** Start with 2-3 max. Only create more as needed.

## Success Metrics

After completing this tutorial, you should be able to:

- ✅ Create and manage 3+ parallel worktrees
- ✅ Switch between features in < 5 seconds (no stashing)
- ✅ Run simultaneous AI sessions (one per feature)
- ✅ Access shared specs from any worktree
- ✅ Complete features independently without blocking
- ✅ Clean up completed worktrees
- ✅ Maintain clean main branch throughout development

## Next Steps

1. **Practice:** Create 2-3 worktrees for your current project
2. **Experiment:** Try running tests in parallel across worktrees
3. **Optimize:** Set up shell aliases for quick worktree switching
4. **Scale:** Use worktrees for all new features
5. **Share:** Teach your team the worktree workflow

## Related Resources

- [Git Worktree User Guide](README.md) - Complete reference
- [Quickstart Guide](../05_quickstart/readme.md) - Basic SpecKit Plus workflow
- [Core Commands](../06_core_commands/readme.md) - All `/sp.*` commands
- [SpecKit Plus Tests](../../tests/worktree/README.md) - Verify your setup

## Key Takeaways

🎯 **Context Preservation:** Never lose work when switching features
🎯 **Parallel Development:** Work on 2-3 features simultaneously
🎯 **Shared Knowledge:** Specs and history accessible from all worktrees
🎯 **Clean Main:** Main branch always deployable
🎯 **AI-Friendly:** Each worktree can have its own AI session
🎯 **Team-Ready:** Mix worktree and traditional workflows

**Remember:** Worktrees are a tool, not a requirement. Use them when you need parallel development. For single-feature work, the traditional workflow is perfectly fine!

---

**Ready to level up?** Try the [Advanced Worktree Patterns](02_advanced_patterns.md) tutorial next.
