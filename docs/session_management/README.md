# Session Management

## Purpose
This directory tracks all development sessions to ensure continuity, prevent loss of progress during context window resets, and maintain a complete audit trail of the project.

## Critical Files

### `next_session_plan.md` (ROOT LEVEL - MOST IMPORTANT)
**Location**: `/Users/wadew/Code/gitlab_mcp/next_session_plan.md`

This is THE critical handoff document. At the start of any new session after context reset:
1. Read `CLAUDE.md` for ground rules
2. Read `next_session_plan.md` for current state and next steps

This file MUST be updated before ending any session where significant work was completed.

### Session Archive
- `session_index.md` - Index of all completed sessions
- `sessions/session_XXX_YYYY-MM-DD.md` - Completed session logs (archived)

## Session Workflow

### Start of Session (After Context Reset)
1. Read `/Users/wadew/Code/gitlab_mcp/CLAUDE.md` - Ground rules and project standards
2. Read `/Users/wadew/Code/gitlab_mcp/next_session_plan.md` - Current state and plan
3. Review current phase documentation in `docs/phases/`
4. Check coverage status and test results

### During Session
- Follow TDD process (write tests first)
- Update code
- Run tests continuously
- Document decisions and issues

### End of Session (Before Context Reset)
1. Archive current session to `sessions/session_XXX_YYYY-MM-DD.md`
2. Update `session_index.md` with session entry
3. **CRITICAL**: Update `/Users/wadew/Code/gitlab_mcp/next_session_plan.md` with:
   - Current phase and progress
   - What was completed
   - Current test coverage
   - Blockers/issues
   - Exact next steps
4. Ensure all tests are passing
5. Commit code if at a stable checkpoint

## Session Log Format

Each archived session includes:
- **Session Metadata**: Number, date, phase
- **Objectives**: What was planned
- **Work Completed**: What was actually done
- **Tests**: Tests written, coverage achieved, pass rate
- **Files Modified**: Complete list of changed files
- **Issues/Blockers**: Problems encountered
- **Decisions**: Important technical decisions made
- **Next Steps**: What should happen next (detailed)

## Phase Gate Tracking

Before moving to next phase, verify:
- [ ] All phase tests written (TDD)
- [ ] All tests passing (100%)
- [ ] Phase coverage ≥ 80%
- [ ] Phase documentation complete
- [ ] Session log updated
- [ ] next_session_plan.md updated

## Coverage Tracking

Each session should track:
- Overall project coverage percentage
- Per-module coverage
- Uncovered lines needing tests
- Coverage trend (increasing/decreasing)

## Tips

- Update `next_session_plan.md` frequently, not just at session end
- Be specific in next steps (file names, function names, test descriptions)
- Include command examples for running tests
- Note any environment setup or configuration changes
- Reference specific line numbers for incomplete work
