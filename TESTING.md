# Testing SpecKit Plus Locally

This guide shows how to test the worktree and review features offline without needing a full installation.

## 🚀 Quick Start (Recommended)

### Option 1: Automated Test + Demo

```bash
# Run comprehensive automated tests + create working demo
./test-local-installation.sh
```

This will:
- ✅ Run all 70 automated tests
- ✅ Create a real test project
- ✅ Create 2 worktrees with specs
- ✅ Run all review modes
- ✅ Show you exactly what was created

**Time:** ~2-3 minutes

### Option 2: Interactive Demo

```bash
# Step-by-step interactive demonstration
./demo-worktree-review.sh
```

This will:
- ✅ Walk you through each feature
- ✅ Show worktree creation
- ✅ Demonstrate shared specs
- ✅ Run code reviews
- ✅ Show multi-agent reviews

**Time:** ~5-10 minutes (you control the pace)

---

## 📋 Testing Scripts

### `test-local-installation.sh`

**What it does:**
1. Runs all 70 automated tests (worktree + review)
2. Creates a test project with SpecKit Plus
3. Creates 2 worktrees for parallel development
4. Verifies shared specs/ and history/
5. Tests all review modes (quick/thorough/security/performance)
6. Validates multi-agent support
7. Checks JSON output format

**Usage:**
```bash
./test-local-installation.sh
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SpecKit Plus Local Installation Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Running automated test suites...
✓ Worktree tests passed (31 tests)
✓ Review tests passed (39 tests)
✓ All 70 tests passed!

Step 2: Creating test project...
✓ Test project created

Step 3: Testing worktree functionality...
✓ Worktree created: worktrees/001-user-authentication
✓ Second worktree created: worktrees/002-task-management

Step 4: Testing shared specs/history...
✓ Spec from worktree 1 is accessible in worktree 2
✓ get_repo_root() returns main repo path

Step 5: Testing review command...
✓ Review directory created
✓ Context file created
✓ Review template created
✓ Security review mode works
✓ Thorough review mode works
✓ Performance review mode works
✓ JSON output is valid
✓ Agent parameter works

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ All tests passed! Local installation works correctly.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### `demo-worktree-review.sh`

**What it does:**
Interactive step-by-step demo showing:
- Part 1: Creating parallel worktrees
- Part 2: Shared specs & history
- Part 3: AI-assisted code review
- Part 4: Multiple review modes
- Part 5: Multi-agent reviews

**Usage:**
```bash
./demo-worktree-review.sh
```

Press Enter to advance through each step. You'll see exactly what happens at each stage.

---

## 🧪 Manual Testing

If you want to test specific features:

### Test Worktree Creation

```bash
# Create test project
mkdir ~/test-worktree && cd ~/test-worktree
git init
git config user.email "test@example.com"
git config user.name "Test"

# Copy scripts
cp -r /home/user/spec-kit-plus/scripts .
mkdir -p specs history
echo "# Constitution" > history/constitution.md
git add . && git commit -m "Initial"

# Enable worktree mode
export SPECIFY_WORKTREE_MODE=true

# Create worktree
bash scripts/bash/create-new-feature.sh
# Enter: "my feature"

# Verify
git worktree list
ls ../worktrees/
```

### Test Review Command

```bash
# In a feature branch with spec and plan
cd /path/to/feature-branch

# Create spec
mkdir -p specs/001-feature
echo "# Spec" > specs/001-feature/spec.md
echo "# Plan" > specs/001-feature/plan.md

# Run review
bash /home/user/spec-kit-plus/scripts/bash/review-implementation.sh --mode quick

# Check output
ls -la specs/001-feature/reviews/
```

### Test Shared Specs

```bash
# In worktree 1
cd worktrees/001-feature
mkdir -p ../../main-repo/specs/001-feature
echo "# Test" > ../../main-repo/specs/001-feature/spec.md

# In worktree 2
cd ../002-other-feature
cat ../../main-repo/specs/001-feature/spec.md
# Should show: # Test
```

---

## 🔬 Running Individual Test Suites

### Worktree Tests Only
```bash
cd tests/worktree
./run-all-tests.sh
```

**What it tests:**
- Worktree detection (6 tests)
- Worktree management (6 tests)
- Integration with SpecKit (4 tests)
- Edge cases (4 tests)

### Review Tests Only
```bash
cd tests/review
./run-all-tests.sh
```

**What it tests:**
- Script validation (3 tests)
- Mode detection (4 tests)
- File creation (5 tests)
- Agent support (2 tests)
- JSON output (1 test)
- Error handling (3 tests)
- Optional content (3 tests)
- Template structure (2 tests)

---

## 🎯 What Gets Tested

### Worktree Functionality (31 tests)
| Category | Tests | What's Verified |
|----------|-------|-----------------|
| Detection | 6 | `is_worktree()`, `get_repo_root()` |
| Management | 6 | Create, list, remove worktrees |
| Integration | 4 | Specs shared, history shared |
| Edge Cases | 4 | Nested worktrees, empty names |
| **Bash** | **20** | All bash functionality |
| **PowerShell** | **11** | All PowerShell functionality |

### Review Functionality (39 tests)
| Category | Tests | What's Verified |
|----------|-------|-----------------|
| Script Validation | 3 | Script exists, help works |
| Mode Detection | 4 | All 4 review modes |
| File Creation | 5 | Context & review files |
| Agent Support | 2 | Custom and default agents |
| JSON Output | 1 | Valid JSON format |
| Error Handling | 3 | Missing spec/plan/branch |
| Optional Content | 3 | Tasks, data model inclusion |
| Template | 2 | Structure, checklists |
| **Bash** | **25** | All bash functionality |
| **PowerShell** | **14** | All PowerShell functionality |

---

## 📊 Expected Results

### All Tests Pass
```
Tests Run:    70
Tests Passed: 70
Tests Failed: 0

✓ All tests passed!
```

### Individual Features Work
- ✅ Worktrees created in `../worktrees/` directory
- ✅ `get_repo_root()` returns main repo (not worktree)
- ✅ Specs accessible from all worktrees
- ✅ Review creates context + template files
- ✅ All 4 review modes functional
- ✅ Multi-agent reviews work
- ✅ JSON output valid

---

## 🐛 Troubleshooting

### Tests Fail
```bash
# Run with verbose output
cd tests/worktree
./test-worktree.sh --verbose

# Or keep test artifacts
./run-all-tests.sh --keep
ls /tmp/speckit-worktree-tests/
```

### "Git version too old"
```bash
git --version  # Need 2.15+
# Update git if needed
```

### "PowerShell tests skipped"
This is fine - PowerShell is optional. Bash tests cover the same functionality.

### Demo script fails
```bash
# Check you're in the repo root
cd /home/user/spec-kit-plus
./demo-worktree-review.sh

# Or run automated test instead
./test-local-installation.sh
```

---

## 🔍 Inspecting Test Projects

After running tests, you can explore the created projects:

```bash
# After test-local-installation.sh
cd ~/speckit-test-*  # Tab-complete
tree -L 3

# Check worktrees
git worktree list

# View specs
cat specs/*/spec.md

# View reviews
ls specs/001-*/reviews/
cat specs/001-*/reviews/*_context.md
```

---

## 📚 Next Steps

After verifying everything works:

1. **Read the tutorials:**
   - `docs-plus/04_git_worktrees/01_multi_session_workflow.md`
   - `docs-plus/04_git_worktrees/02_advanced_patterns.md`
   - `docs-plus/06_core_commands/10_review/readme.md`

2. **Try in a real project:**
   ```bash
   cd your-project
   cp -r /home/user/spec-kit-plus/scripts .
   cp -r /home/user/spec-kit-plus/templates .
   ```

3. **Run the full test suite:**
   ```bash
   ./test-local-installation.sh
   ```

---

## 💡 Tips

### Quick Validation
```bash
# Just run the tests (fastest)
cd tests && ./worktree/run-all-tests.sh && ./review/run-all-tests.sh
```

### Full Experience
```bash
# Interactive demo (best for understanding)
./demo-worktree-review.sh
```

### Comprehensive Check
```bash
# Automated test + real usage (most thorough)
./test-local-installation.sh
```

---

## 📝 Summary

| Script | Time | What You Get |
|--------|------|--------------|
| **test-local-installation.sh** | 2-3 min | Automated validation + working demo |
| **demo-worktree-review.sh** | 5-10 min | Interactive walkthrough |
| **tests/worktree/run-all-tests.sh** | 30-45s | 31 worktree tests |
| **tests/review/run-all-tests.sh** | 30-45s | 39 review tests |

**Recommended:** Start with `./test-local-installation.sh` for quick validation, then `./demo-worktree-review.sh` to see features in action.

---

## 🎉 Success Criteria

You know everything works when:

✅ All 70 tests pass
✅ Worktrees created successfully
✅ `get_repo_root()` returns main repo path
✅ Specs shared across worktrees
✅ Review creates context + template files
✅ All review modes work
✅ Multi-agent support functional

If all these pass, the implementation is ready! 🚀
