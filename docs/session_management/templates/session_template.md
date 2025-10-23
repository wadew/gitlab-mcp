# Session XXX - YYYY-MM-DD

## Session Metadata
- **Session Number**: XXX
- **Date**: YYYY-MM-DD
- **Phase**: Phase N - [Phase Name]
- **Duration**: [Start Time] - [End Time]
- **Previous Session**: [Link to previous session]

## Objectives
What was planned for this session:
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Work Completed
What was actually accomplished:

### Code Changes
- [List of features/functions implemented]
- [Refactorings completed]

### Tests Written
- [Test file 1]: [Brief description]
  - Test count: X
  - All passing: Yes/No
- [Test file 2]: [Brief description]
  - Test count: X
  - All passing: Yes/No

### Documentation Updated
- [Doc file 1]: [What was added/changed]
- [Doc file 2]: [What was added/changed]

## Test Results

### Coverage
```
Overall Coverage: XX.X%
Previous Coverage: XX.X%
Change: +/-X.X%

Module Coverage:
- src/gitlab_mcp/config: XX.X%
- src/gitlab_mcp/client: XX.X%
- src/gitlab_mcp/tools: XX.X%
```

### Test Execution
```
Total Tests: XX
Passed: XX
Failed: XX
Skipped: XX
Pass Rate: XX.X%
```

### Uncovered Lines
```
[File path]: Lines [X-Y, Z]
[File path]: Lines [X-Y, Z]
```

## Files Modified
Complete list of all files created or changed:

### Created
- `path/to/file1.py`
- `path/to/file2.py`

### Modified
- `path/to/file3.py` - [Brief description of changes]
- `path/to/file4.py` - [Brief description of changes]

### Deleted
- `path/to/old_file.py` - [Reason for deletion]

## Issues & Blockers

### Resolved
- **Issue**: [Description]
  - **Resolution**: [How it was fixed]

### Open/Blocked
- **Issue**: [Description]
  - **Impact**: [What is blocked]
  - **Next Steps**: [What needs to happen]

## Technical Decisions
Important decisions made during this session:

1. **Decision**: [Description]
   - **Rationale**: [Why this was chosen]
   - **Alternatives Considered**: [Other options]
   - **Impact**: [What this affects]

## Lessons Learned
- [Learning 1]
- [Learning 2]

## Phase Gate Status
- [ ] All phase tests written (TDD)
- [ ] All tests passing (100%)
- [ ] Phase coverage ≥ 80%
- [ ] Phase documentation complete
- [ ] Session log updated
- [ ] next_session_plan.md updated

## Next Steps
Detailed plan for next session (also in next_session_plan.md):

1. **Immediate Next Task**: [Very specific task with file/function names]
2. **Following Tasks**: [Priority ordered list]
3. **Testing Focus**: [What needs test coverage]
4. **Documentation Needs**: [What docs to update]

## Commands for Next Session
```bash
# Run tests
pytest tests/ -v --cov=src/gitlab_mcp --cov-report=term-missing

# Check coverage
coverage report

# Run specific test file
pytest tests/unit/test_config/test_settings.py -v
```

## References
- PRD: `docs/gitlab-mcp-server-prd.md`
- Phase Doc: `docs/phases/phase_X_name.md`
- API Reference: `docs/api/tools_reference.md`
- Related Issues: [Links if applicable]

---
**Next Session**: [Link when available]
