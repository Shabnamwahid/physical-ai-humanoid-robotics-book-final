# History/Prompts System

## Philosophy

This system implements **spec-driven development** for the Physical AI & Humanoid Robotics textbook project, ensuring complete transparency and reproducibility of all development processes. Every change, decision, and implementation is traced through standardized prompt files that document the entire evolution of the project.

## Core Stages

The system follows a standardized workflow with these stages:

1. **constitution** - Establishing structure, principles, and foundational decisions
2. **spec** - Detailed specifications and requirements
3. **plan** - Implementation plans and strategies
4. **tasks** - Specific task breakdowns and assignments
5. **green** - Implementation stage (successful completion)
6. **clarify** - Clarification and refinement of requirements
7. **analyze** - Analysis and evaluation of implementations
8. **checklist** - Verification and quality assurance

## Naming Convention

All prompt files follow the standardized format:
```
{sequence}-{description}.{stage}.prompt.md
```

Where:
- `{sequence}`: 3-digit zero-padded number (000, 001, 002, etc.)
- `{description}`: Short descriptive name for the task
- `{stage}`: One of the 8 core stages above
- `.prompt.md`: Standard extension for all prompt files

## Frontmatter Template

All prompt files must include the following frontmatter:

```yaml
---
# Document Classification
stage: constitution | spec | plan | tasks | green | clarify | analyze | checklist
status: draft | review | approved | completed | archived
type: feature | bug | refactor | research | documentation | infrastructure
priority: critical | high | medium | low
category: ai | robotics | simulation | curriculum | tooling

# Timeline & Metadata
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
author: author_name
reviewers:
  - reviewer1
  - reviewer2

# Dependencies & Links
depends_on:
  - path/to/dependency.file
related_to:
  - path/to/related.file
blocks:
  - path/to/blocked/file

# Implementation Tracking
assigned_to: team_member
estimated_duration: hours
actual_duration: hours
completion_criteria:
  - criterion1
  - criterion2
  - criterion3

# Validation & Quality
test_strategy: unit | integration | system | manual
review_required: true | false
sign_off_required: true | false
---
```

## Directory Structure

```
history/prompts/
├── README.md                 # This file
├── general/                  # General project prompts
├── chapter-1/               # Chapter 1 specific prompts
├── chapter-2/               # Chapter 2 specific prompts
├── chapter-3/               # Chapter 3 specific prompts
├── chapter-4/               # Chapter 4 specific prompts
├── physical-ai-book/        # Book-wide prompts
└── templates/               # Template files (optional)
```

## Guidelines for Use

### Creating New Prompt Files

1. **Choose appropriate directory**: Place chapter-specific prompts in the relevant chapter folder
2. **Select next sequence number**: Use the next available number in the sequence
3. **Use descriptive names**: Make the description clear and specific
4. **Include complete frontmatter**: Use the template above with all relevant information
5. **Document dependencies**: List any files this prompt depends on or relates to

### Stage Transitions

- Move files between stages as work progresses
- Update status and metadata as implementation evolves
- Maintain clear audit trail of all changes
- Use version control to track modifications

### Best Practices

- **Be specific**: Use clear, descriptive names for prompts
- **Maintain consistency**: Follow the naming and structure conventions
- **Document thoroughly**: Include all relevant metadata in frontmatter
- **Track dependencies**: Maintain clear links between related prompts
- **Regular reviews**: Update status and completion criteria regularly
- **Cross-reference**: Link related prompts and files appropriately

## Quality Standards

### Content Requirements

- Clear, unambiguous instructions
- Complete context and background information
- Specific, measurable success criteria
- Well-defined dependencies and constraints

### Metadata Requirements

- Complete frontmatter with all required fields
- Accurate status and priority information
- Proper categorization and tagging
- Valid references to related files

## Integration with Development Workflow

This system integrates with the broader development workflow by:

- Providing traceability from requirements to implementation
- Enabling systematic review and approval processes
- Facilitating collaboration through clear documentation
- Supporting reproducible development practices
- Maintaining comprehensive project history

## Version Control Integration

All prompt files are tracked in version control, with:

- Atomic commits for each prompt file
- Clear commit messages referencing prompt purpose
- Branching strategy aligned with implementation phases
- Tagging system for major milestones