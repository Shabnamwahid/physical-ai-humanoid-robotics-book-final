#!/usr/bin/env bash
#
# Comprehensive Docker-based testing for SpecKit Plus PR #31
# Tests both old flow (traditional branches) and new flow (git worktrees)
# across multiple OS environments and Python versions
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRANCH_NAME="${1:-claude/add-git-tress-setup-01RnSkuVGnzWXsH89EhTgU5R}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $*"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

# Test results tracking
declare -a PASSED_TESTS=()
declare -a FAILED_TESTS=()

record_pass() {
    PASSED_TESTS+=("$1")
    log_success "$1"
}

record_fail() {
    FAILED_TESTS+=("$1")
    log_error "$1"
}

# ============================================================================
# Test 1: Ubuntu 22.04 - Old Flow (Traditional Branches)
# ============================================================================
test_ubuntu_old_flow() {
    log_info "Testing OLD FLOW on Ubuntu 22.04 (Traditional Branch Workflow)"

    local container_name="speckit-test-ubuntu-old-$$"

    if docker run --rm --name "$container_name" \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        ubuntu:22.04 bash -c '
        set -e
        export DEBIAN_FRONTEND=noninteractive

        # Install dependencies
        apt-get update -qq
        apt-get install -y -qq git python3 python3-pip curl > /dev/null 2>&1

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"
        git config --global init.defaultBranch main

        # Create a fresh test project (Calculator from docs)
        cd /tmp
        mkdir calculator-test && cd calculator-test
        git init

        # Initialize SpecKit (old flow - no worktrees)
        unset SPECIFY_WORKTREE_MODE

        # Create .specify directory structure
        mkdir -p .specify
        cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
        cp -r /workspace/scripts ./ 2>/dev/null || true
        cp -r /workspace/templates ./ 2>/dev/null || true
        mkdir -p specs history

        # Initial commit
        echo "# Calculator Project" > README.md
        git add .
        git commit -m "Initial commit" > /dev/null 2>&1

        # Test: Create first feature (001-basic-operations)
        echo "Creating feature: basic calculator operations" | \
            bash scripts/bash/create-new-feature.sh --short-name "basic-ops" > /dev/null 2>&1

        # Verify branch created
        if ! git rev-parse --verify 001-basic-ops > /dev/null 2>&1; then
            echo "ERROR: Branch 001-basic-ops not created"
            exit 1
        fi

        # Verify on correct branch
        CURRENT=$(git rev-parse --abbrev-ref HEAD)
        if [ "$CURRENT" != "001-basic-ops" ]; then
            echo "ERROR: Not on branch 001-basic-ops (on: $CURRENT)"
            exit 1
        fi

        # Verify spec directory created
        if [ ! -d "specs/001-basic-ops" ]; then
            echo "ERROR: Spec directory not created"
            exit 1
        fi

        # Test: Create second feature (002-advanced-operations)
        git checkout main > /dev/null 2>&1
        echo "Creating feature: advanced operations" | \
            bash scripts/bash/create-new-feature.sh --short-name "advanced-ops" > /dev/null 2>&1

        # Verify correct numbering
        if ! git rev-parse --verify 002-advanced-ops > /dev/null 2>&1; then
            echo "ERROR: Branch 002-advanced-ops not created (numbering failed)"
            exit 1
        fi

        # Verify no worktrees created (old flow)
        WORKTREE_COUNT=$(git worktree list | wc -l)
        if [ "$WORKTREE_COUNT" -ne 1 ]; then
            echo "ERROR: Worktrees created in old flow (should only have main)"
            exit 1
        fi

        echo "SUCCESS: Old flow works perfectly on Ubuntu"
    '; then
        record_pass "Ubuntu 22.04 - Old Flow (Traditional Branches)"
        return 0
    else
        record_fail "Ubuntu 22.04 - Old Flow (Traditional Branches)"
        return 1
    fi
}

# ============================================================================
# Test 2: Ubuntu 22.04 - New Flow (Git Worktrees)
# ============================================================================
test_ubuntu_new_flow() {
    log_info "Testing NEW FLOW on Ubuntu 22.04 (Git Worktree Multi-session)"

    local container_name="speckit-test-ubuntu-new-$$"

    if docker run --rm --name "$container_name" \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        ubuntu:22.04 bash -c '
        set -e
        export DEBIAN_FRONTEND=noninteractive

        # Install dependencies
        apt-get update -qq
        apt-get install -y -qq git python3 python3-pip curl > /dev/null 2>&1

        # Check git version supports worktrees (2.5+)
        GIT_VERSION=$(git --version | sed -n "s/^git version \([0-9]*\.[0-9]*\).*/\1/p")
        GIT_MAJOR=$(echo "$GIT_VERSION" | cut -d. -f1)
        GIT_MINOR=$(echo "$GIT_VERSION" | cut -d. -f2)

        if [ "$GIT_MAJOR" -lt 2 ] || { [ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 5 ]; }; then
            echo "WARNING: Git version too old for worktrees ($GIT_VERSION < 2.5)"
            exit 0
        fi

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"
        git config --global init.defaultBranch main

        # Create a fresh test project
        cd /tmp
        mkdir ecommerce-test && cd ecommerce-test
        git init

        # Initialize SpecKit (NEW FLOW - with worktrees)
        export SPECIFY_WORKTREE_MODE=true

        # Create .specify directory structure
        mkdir -p .specify
        cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
        cp -r /workspace/scripts ./ 2>/dev/null || true
        cp -r /workspace/templates ./ 2>/dev/null || true
        mkdir -p specs history

        # Initial commit
        echo "# E-commerce Project" > README.md
        git add .
        git commit -m "Initial commit" > /dev/null 2>&1

        # Test: Create first feature with worktree (001-user-auth)
        echo "Creating feature: user authentication" | \
            bash scripts/bash/create-new-feature.sh --short-name "user-auth" > /dev/null 2>&1

        # Verify worktree created
        if [ ! -d "../001-user-auth" ]; then
            echo "ERROR: Worktree directory not created"
            exit 1
        fi

        # Verify branch created
        if ! git rev-parse --verify 001-user-auth > /dev/null 2>&1; then
            echo "ERROR: Branch 001-user-auth not created"
            exit 1
        fi

        # Verify spec directory created in MAIN repo (shared)
        if [ ! -d "specs/001-user-auth" ]; then
            echo "ERROR: Spec directory not created in main repo"
            exit 1
        fi

        # Verify specs directory is SHARED (accessible from worktree)
        if [ ! -d "../001-user-auth/specs/001-user-auth" ]; then
            echo "ERROR: Specs not accessible from worktree"
            exit 1
        fi

        # Test: Create second feature in parallel (002-product-catalog)
        echo "Creating feature: product catalog" | \
            bash scripts/bash/create-new-feature.sh --short-name "product-catalog" > /dev/null 2>&1

        # Verify second worktree
        if [ ! -d "../002-product-catalog" ]; then
            echo "ERROR: Second worktree not created"
            exit 1
        fi

        # Verify we have 3 worktrees (main + 2 features)
        WORKTREE_COUNT=$(git worktree list | wc -l)
        if [ "$WORKTREE_COUNT" -ne 3 ]; then
            echo "ERROR: Expected 3 worktrees, got $WORKTREE_COUNT"
            exit 1
        fi

        # Test: Verify both worktrees can access shared specs
        cd ../001-user-auth
        if [ ! -d "specs/002-product-catalog" ]; then
            echo "ERROR: Worktree 001 cannot see specs from 002"
            exit 1
        fi

        cd ../002-product-catalog
        if [ ! -d "specs/001-user-auth" ]; then
            echo "ERROR: Worktree 002 cannot see specs from 001"
            exit 1
        fi

        # Test: Verify worktree cleanup
        cd ../ecommerce-test
        bash scripts/bash/create-new-feature.sh --cleanup 001-user-auth > /dev/null 2>&1

        if [ -d "../001-user-auth" ]; then
            echo "ERROR: Worktree cleanup failed"
            exit 1
        fi

        # Verify we now have 2 worktrees (main + 1 feature)
        WORKTREE_COUNT=$(git worktree list | wc -l)
        if [ "$WORKTREE_COUNT" -ne 2 ]; then
            echo "ERROR: Expected 2 worktrees after cleanup, got $WORKTREE_COUNT"
            exit 1
        fi

        echo "SUCCESS: New flow (worktrees) works perfectly on Ubuntu"
    '; then
        record_pass "Ubuntu 22.04 - New Flow (Git Worktrees)"
        return 0
    else
        record_fail "Ubuntu 22.04 - New Flow (Git Worktrees)"
        return 1
    fi
}

# ============================================================================
# Test 3: Alpine Linux - Old Flow
# ============================================================================
test_alpine_old_flow() {
    log_info "Testing OLD FLOW on Alpine Linux (Minimal Environment)"

    local container_name="speckit-test-alpine-old-$$"

    if docker run --rm --name "$container_name" \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        alpine:latest bash -c '
        set -e

        # Install dependencies (minimal)
        apk add --no-cache git bash python3 py3-pip curl > /dev/null 2>&1

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"
        git config --global init.defaultBranch main

        # Create test project
        cd /tmp
        mkdir blog-test && cd blog-test
        git init

        # Initialize SpecKit (old flow)
        unset SPECIFY_WORKTREE_MODE

        mkdir -p .specify
        cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
        cp -r /workspace/scripts ./ 2>/dev/null || true
        cp -r /workspace/templates ./ 2>/dev/null || true
        mkdir -p specs history

        echo "# Blog Platform" > README.md
        git add .
        git commit -m "Initial commit" > /dev/null 2>&1

        # Create feature
        echo "Creating feature: article management" | \
            bash scripts/bash/create-new-feature.sh --short-name "articles" > /dev/null 2>&1

        # Verify
        if ! git rev-parse --verify 001-articles > /dev/null 2>&1; then
            echo "ERROR: Branch creation failed on Alpine"
            exit 1
        fi

        if [ ! -d "specs/001-articles" ]; then
            echo "ERROR: Spec directory not created on Alpine"
            exit 1
        fi

        echo "SUCCESS: Old flow works on Alpine Linux"
    ' 2>&1; then
        record_pass "Alpine Linux - Old Flow"
        return 0
    else
        record_fail "Alpine Linux - Old Flow"
        return 1
    fi
}

# ============================================================================
# Test 4: Alpine Linux - New Flow
# ============================================================================
test_alpine_new_flow() {
    log_info "Testing NEW FLOW on Alpine Linux (Git Worktrees)"

    local container_name="speckit-test-alpine-new-$$"

    if docker run --rm --name "$container_name" \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        alpine:latest bash -c '
        set -e

        # Install dependencies
        apk add --no-cache git bash python3 py3-pip curl > /dev/null 2>&1

        # Check git version
        GIT_VERSION=$(git --version | sed -n "s/^git version \([0-9]*\.[0-9]*\).*/\1/p")
        GIT_MAJOR=$(echo "$GIT_VERSION" | cut -d. -f1)
        GIT_MINOR=$(echo "$GIT_VERSION" | cut -d. -f2)

        if [ "$GIT_MAJOR" -lt 2 ] || { [ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 5 ]; }; then
            echo "WARNING: Git too old for worktrees on Alpine"
            exit 0
        fi

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"
        git config --global init.defaultBranch main

        # Create test project
        cd /tmp
        mkdir cms-test && cd cms-test
        git init

        export SPECIFY_WORKTREE_MODE=true

        mkdir -p .specify
        cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
        cp -r /workspace/scripts ./ 2>/dev/null || true
        cp -r /workspace/templates ./ 2>/dev/null || true
        mkdir -p specs history

        echo "# CMS Platform" > README.md
        git add .
        git commit -m "Initial commit" > /dev/null 2>&1

        # Create worktree feature
        echo "Creating feature: content management" | \
            bash scripts/bash/create-new-feature.sh --short-name "content" > /dev/null 2>&1

        # Verify worktree
        if [ ! -d "../001-content" ]; then
            echo "ERROR: Worktree not created on Alpine"
            exit 1
        fi

        if ! git rev-parse --verify 001-content > /dev/null 2>&1; then
            echo "ERROR: Branch not created on Alpine"
            exit 1
        fi

        # Verify shared specs
        if [ ! -d "../001-content/specs/001-content" ]; then
            echo "ERROR: Shared specs not working on Alpine"
            exit 1
        fi

        echo "SUCCESS: New flow (worktrees) works on Alpine Linux"
    ' 2>&1; then
        record_pass "Alpine Linux - New Flow (Git Worktrees)"
        return 0
    else
        record_fail "Alpine Linux - New Flow (Git Worktrees)"
        return 1
    fi
}

# ============================================================================
# Test 5: Python Version Compatibility
# ============================================================================
test_python_versions() {
    log_info "Testing Python 3.9, 3.10, 3.11, 3.12 compatibility"

    local versions=("3.9" "3.10" "3.11" "3.12")
    local all_passed=true

    for version in "${versions[@]}"; do
        log_info "Testing with Python $version"

        if docker run --rm \
            -v "$REPO_ROOT:/workspace" \
            -w /workspace \
            "python:$version-slim" bash -c '
            set -e

            # Install git
            apt-get update -qq
            apt-get install -y -qq git > /dev/null 2>&1

            # Configure git
            git config --global user.name "Test User"
            git config --global user.email "test@example.com"
            git config --global init.defaultBranch main

            # Test basic script execution
            cd /tmp
            mkdir py-test && cd py-test
            git init

            mkdir -p .specify
            cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
            cp -r /workspace/scripts ./ 2>/dev/null || true
            cp -r /workspace/templates ./ 2>/dev/null || true
            mkdir -p specs history

            echo "# Python Test" > README.md
            git add .
            git commit -m "Initial commit" > /dev/null 2>&1

            # Test feature creation
            echo "Creating feature" | \
                bash scripts/bash/create-new-feature.sh --short-name "test-feature" > /dev/null 2>&1

            if [ ! -d "specs/001-test-feature" ]; then
                echo "ERROR: Feature creation failed"
                exit 1
            fi

            echo "SUCCESS: Python compatibility OK"
        ' 2>&1; then
            record_pass "Python $version - Compatibility"
        else
            record_fail "Python $version - Compatibility"
            all_passed=false
        fi
    done

    if $all_passed; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# Test 6: Edge Cases in Clean Environment
# ============================================================================
test_edge_cases() {
    log_info "Testing edge cases in clean Docker environment"

    if docker run --rm \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        ubuntu:22.04 bash -c '
        set -e
        export DEBIAN_FRONTEND=noninteractive

        # Install dependencies
        apt-get update -qq
        apt-get install -y -qq git bash > /dev/null 2>&1

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"
        git config --global init.defaultBranch main

        cd /tmp
        mkdir edge-test && cd edge-test
        git init

        mkdir -p .specify
        cp -r /workspace/.specify/* .specify/ 2>/dev/null || true
        cp -r /workspace/scripts ./ 2>/dev/null || true
        cp -r /workspace/templates ./ 2>/dev/null || true
        mkdir -p specs history

        echo "# Edge Case Tests" > README.md
        git add .
        git commit -m "Initial commit" > /dev/null 2>&1

        # Edge Case 1: Branch name with spaces (should fail gracefully)
        echo "Testing: branch name validation"
        if echo "test feature" | bash scripts/bash/create-new-feature.sh --short-name "test feature" 2>&1 | grep -q "cannot contain spaces"; then
            echo "✓ Space validation works"
        else
            echo "ERROR: Space validation failed"
            exit 1
        fi

        # Edge Case 2: Very long branch name (should fail gracefully)
        echo "Testing: long branch name validation"
        LONG_NAME=$(printf "a%.0s" {1..250})
        if echo "test" | bash scripts/bash/create-new-feature.sh --short-name "$LONG_NAME" 2>&1 | grep -q "too long"; then
            echo "✓ Length validation works"
        else
            echo "ERROR: Length validation failed"
            exit 1
        fi

        # Edge Case 3: Detached HEAD (should fail gracefully)
        echo "Testing: detached HEAD detection"
        git checkout HEAD~0 > /dev/null 2>&1
        if echo "test" | bash scripts/bash/create-new-feature.sh --short-name "test" 2>&1 | grep -q "detached HEAD"; then
            echo "✓ Detached HEAD detection works"
        else
            echo "ERROR: Detached HEAD detection failed"
            exit 1
        fi
        git checkout main > /dev/null 2>&1

        # Edge Case 4: Missing specs directory (should auto-create)
        echo "Testing: auto-create missing specs directory"
        rm -rf specs
        echo "test" | bash scripts/bash/create-new-feature.sh --short-name "auto-test" > /dev/null 2>&1
        if [ -d "specs/001-auto-test" ]; then
            echo "✓ Auto-create specs directory works"
        else
            echo "ERROR: Auto-create failed"
            exit 1
        fi

        # Edge Case 5: Numbering with leading zeros (01, 010 → 011)
        echo "Testing: numbering with leading zeros"
        git checkout main > /dev/null 2>&1
        mkdir -p specs/01-test specs/010-test
        echo "test" | bash scripts/bash/create-new-feature.sh --short-name "next" > /dev/null 2>&1
        if [ -d "specs/011-next" ]; then
            echo "✓ Numbering fix works (01, 010 → 011)"
        else
            echo "ERROR: Numbering failed"
            ls -la specs/
            exit 1
        fi

        echo "SUCCESS: All edge cases handled correctly"
    ' 2>&1; then
        record_pass "Edge Cases - Clean Environment"
        return 0
    else
        record_fail "Edge Cases - Clean Environment"
        return 1
    fi
}

# ============================================================================
# Test 7: Automated Test Suite
# ============================================================================
test_automated_suite() {
    log_info "Running automated test suite in Docker"

    if docker run --rm \
        -v "$REPO_ROOT:/workspace" \
        -w /workspace \
        ubuntu:22.04 bash -c '
        set -e
        export DEBIAN_FRONTEND=noninteractive

        # Install dependencies
        apt-get update -qq
        apt-get install -y -qq git bash > /dev/null 2>&1

        # Check git version
        GIT_VERSION=$(git --version | sed -n "s/^git version \([0-9]*\.[0-9]*\).*/\1/p")
        GIT_MAJOR=$(echo "$GIT_VERSION" | cut -d. -f1)
        GIT_MINOR=$(echo "$GIT_VERSION" | cut -d. -f2)

        if [ "$GIT_MAJOR" -lt 2 ] || { [ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 5 ]; }; then
            echo "WARNING: Git too old for worktree tests"
            exit 0
        fi

        # Configure git
        git config --global user.name "Test User"
        git config --global user.email "test@example.com"

        # Run the test suite
        cd /workspace
        bash tests/worktree/test-worktree.sh
    ' 2>&1; then
        record_pass "Automated Test Suite"
        return 0
    else
        record_fail "Automated Test Suite"
        return 1
    fi
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    log_info "========================================="
    log_info "SpecKit Plus PR #31 - Comprehensive Test"
    log_info "Branch: $BRANCH_NAME"
    log_info "========================================="
    echo ""

    # Run all tests
    test_ubuntu_old_flow
    echo ""

    test_ubuntu_new_flow
    echo ""

    test_alpine_old_flow
    echo ""

    test_alpine_new_flow
    echo ""

    test_python_versions
    echo ""

    test_edge_cases
    echo ""

    test_automated_suite
    echo ""

    # Print summary
    log_info "========================================="
    log_info "TEST SUMMARY"
    log_info "========================================="

    if [ ${#PASSED_TESTS[@]} -gt 0 ]; then
        log_success "PASSED TESTS (${#PASSED_TESTS[@]}):"
        for test in "${PASSED_TESTS[@]}"; do
            echo "  ✓ $test"
        done
    fi

    echo ""

    if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
        log_error "FAILED TESTS (${#FAILED_TESTS[@]}):"
        for test in "${FAILED_TESTS[@]}"; do
            echo "  ✗ $test"
        done
        echo ""
        log_error "OVERALL RESULT: FAILED"
        exit 1
    else
        log_success "OVERALL RESULT: ALL TESTS PASSED ✓"
        exit 0
    fi
}

main "$@"
