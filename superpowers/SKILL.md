---
name: superpowers
description: 大项目、需求不明确时调用这个东西
---

# Superpowers

Superpowers is a complete software development methodology for coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them.

## When to Use

- Starting a new project or feature with unclear requirements
- Need structured brainstorming before implementation
- Want TDD-driven development with automated code review
- Managing complex multi-step implementation plans
- Debugging issues that need systematic root-cause analysis

## Basic Workflow

1. **brainstorming** - Refines rough ideas through questions, explores alternatives, presents design for validation
2. **using-git-worktrees** - Creates isolated workspace on new branch
3. **writing-plans** - Breaks work into bite-sized tasks with exact file paths and verification steps
4. **subagent-driven-development** / **executing-plans** - Dispatches fresh subagent per task with two-stage review
5. **test-driven-development** - Enforces RED-GREEN-REFACTOR cycle
6. **requesting-code-review** - Reviews against plan, reports issues by severity
7. **finishing-a-development-branch** - Verifies tests, presents merge/PR/cleanup options

## Skills Library

### Testing
- **test-driven-development** - RED-GREEN-REFACTOR cycle (includes testing anti-patterns reference)

### Debugging
- **systematic-debugging** - 4-phase root cause process (includes root-cause-tracing, defense-in-depth, condition-based-waiting)
- **verification-before-completion** - Ensure it's actually fixed

### Collaboration
- **brainstorming** - Socratic design refinement
- **writing-plans** - Detailed implementation plans
- **executing-plans** - Batch execution with checkpoints
- **dispatching-parallel-agents** - Concurrent subagent workflows
- **requesting-code-review** - Pre-review checklist
- **receiving-code-review** - Responding to feedback
- **using-git-worktrees** - Parallel development branches
- **finishing-a-development-branch** - Merge/PR decision workflow
- **subagent-driven-development** - Fast iteration with two-stage review

### Meta
- **writing-skills** - Create new skills following best practices
- **using-superpowers** - Introduction to the skills system

## Philosophy

- **Test-Driven Development** - Write tests first, always
- **Systematic over ad-hoc** - Process over guessing
- **Complexity reduction** - Simplicity as primary goal
- **Evidence over claims** - Verify before declaring success

See [README.md](README.md) for full documentation and installation guide.
