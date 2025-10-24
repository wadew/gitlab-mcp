# MCP Server - Comprehensive Bug Report & Fix Plan

**Date**: 2025-10-24
**Test Method**: Automated testing script against live GitLab instance
**Test Coverage**: 26/79 tools tested (33%)
**Failure Rate**: 5/26 tools broken (19.2%)

---

## Executive Summary

Automated testing revealed **5 critical bugs** in the 26 tools tested so far. With a **19.2% failure rate** in the tested subset, we can expect **approximately 15 total bugs across all 79 tools**.

The bugs fall into two main categories:
1. **Serialization Errors** (40%) - Python objects not converted to JSON
2. **Type Errors** (60%) - Parameter mismatches and data structure issues

---

## Test Results

### Coverage
- **Total Tools**: 79
- **Tools Tested**: 26 (33%)
- **Tools Passing**: 21 (80.8%)
- **Tools Failing**: 5 (19.2%)
- **Tools Untested**: 53 (67%)

### Untested Tool Categories
The following tools have NOT been tested yet:
- **Merge Request Operations** (11 tools): create, update, merge, close, reopen, approve, unapprove, get_changes, get_commits, get_pipelines
- **Pipeline Operations** (13 tools): get, create, retry, cancel, delete, list_jobs, get_job, get_job_trace, retry_job, cancel_job, play_job, download_artifacts, list_variables
- **Issue Operations** (1 tool): create_issue
- **Label Operations** (3 tools): create, update, delete
- **Milestone Operations** (3 tools): get, create, update
- **Wiki Operations** (4 tools): get, create, update, delete
- **Snippet Operations** (4 tools): get, create, update, delete
- **Release Operations** (4 tools): get, create, update, delete
- **Repository Operations** (4 tools): get_commit, compare_branches, create_branch, delete_branch, create_tag
- **User Operations** (1 tool): list_user_projects (if no test user found)
- **Group Operations** (2 tools): get_group, list_group_members (if no test group found)

---

## Identified Bugs

### Bug #1: projects.get_project - SerializationError
**Status**: 🔴 CRITICAL
**Category**: Serialization Error
**Error**: `Object of type Project is not JSON serializable`

**Root Cause**:
The client method returns a python-gitlab `Project` object directly without converting to dict.

**Location**: `src/gitlab_mcp/client/gitlab_client.py` - `get_project()` method

**Fix**:
```python
# Current (broken):
return project

# Should be:
return project.asdict()
```

**Estimated Effort**: 5 minutes

---

### Bug #2: merge_requests.list_merge_requests - SerializationError
**Status**: 🔴 CRITICAL
**Category**: Serialization Error
**Error**: `Object of type ProjectMergeRequest is not JSON serializable`

**Root Cause**:
Similar to Bug #1 - returns python-gitlab objects without serialization.

**Location**: `src/gitlab_mcp/client/gitlab_client.py` - `list_merge_requests()` method

**Fix**:
Convert all MergeRequest objects to dicts using `.asdict()` before returning.

**Estimated Effort**: 10 minutes

**Note**: This bug likely affects ALL 11 MR-related tools that haven't been tested yet.

---

### Bug #3: projects.search_projects - TypeError
**Status**: 🟡 HIGH
**Category**: Parameter Mismatch
**Error**: `search_projects() got an unexpected keyword argument 'search'`

**Root Cause**:
The tool interface uses parameter name `search` but the client method expects a different parameter name.

**Location**: Tool/client interface mismatch

**Fix**:
1. Check client method signature for correct parameter name
2. Update tool to use correct parameter OR
3. Update client to accept `search` parameter

**Estimated Effort**: 15 minutes

---

### Bug #4: repositories.search_code - TypeError
**Status**: 🟡 HIGH
**Category**: Parameter Mismatch
**Error**: `search_code() got an unexpected keyword argument 'search'`

**Root Cause**:
Same as Bug #3 - parameter name mismatch.

**Location**: Tool/client interface mismatch

**Fix**: Same approach as Bug #3

**Estimated Effort**: 15 minutes

---

### Bug #5: pipelines.list_pipelines - TypeError
**Status**: 🔴 CRITICAL
**Category**: Data Structure Mismatch
**Error**: `string indices must be integers, not 'str'`

**Root Cause**:
- Client returns: `{"pipelines": [...]}`  (dict with nested list)
- Tool expects: Direct iteration over list
- Tool iterates over dict keys (strings) instead of pipeline objects

**Location**:
- Client: `src/gitlab_mcp/client/gitlab_client.py:3870` - returns wrapped dict
- Tool: `src/gitlab_mcp/tools/pipelines.py:44-53` - tries to iterate directly

**Fix Option 1** (Recommended - Fix the tool):
```python
# In tools/pipelines.py:
result = client.list_pipelines(...)
for pipeline in result["pipelines"]:  # Access nested list
    ...
```

**Fix Option 2** (Breaking change - Fix the client):
```python
# In client/gitlab_client.py:
return pipeline_list  # Return unwrapped list
```

**Estimated Effort**: 20 minutes (includes checking all pipeline tools for same pattern)

---

## Potential Additional Bugs

Based on code patterns, these untested tools likely have similar bugs:

### High Probability Bugs:
1. **All MR operation tools** (11 tools) - Likely have serialization errors like list_merge_requests
2. **All pipeline operation tools** (13 tools) - Likely have data structure mismatch like list_pipelines
3. **get_milestone** - Might have serialization error (returns Milestone object)
4. **get_branch** - Might have serialization error (returns Branch object)
5. **get_commit** - Might have serialization error (returns Commit object)
6. **get_tag** - Might have serialization error (returns Tag object)

### Estimated Total Bugs: 15-20 across all 79 tools

---

## Fix Priority

### Priority 1: Immediate (Blocking basic usage)
1. ✅ **Bug #1**: projects.get_project
2. ✅ **Bug #2**: merge_requests.list_merge_requests
3. ✅ **Bug #5**: pipelines.list_pipelines

**Impact**: These tools are fundamental - used for basic project info, MR workflows, and CI/CD monitoring.

**Estimated Time**: 35 minutes

---

### Priority 2: High (Blocking search features)
4. ✅ **Bug #3**: projects.search_projects
5. ✅ **Bug #4**: repositories.search_code

**Impact**: Search functionality is important for code exploration.

**Estimated Time**: 30 minutes

---

### Priority 3: Medium (Expand test coverage)
6. ⏳ **Expand test script** to cover all 79 tools
7. ⏳ **Run comprehensive test** to find remaining bugs
8. ⏳ **Fix all bugs found** in untested tools

**Estimated Time**: 3-4 hours

---

### Priority 4: Low (Quality & Maintenance)
9. ⏳ **Create regression test suite** for CI/CD
10. ⏳ **Update documentation** to reflect working state

**Estimated Time**: 2-3 hours

---

## Fix Plan

### Phase 1: Fix Critical Bugs (1 hour)
1. Fix Bug #1: projects.get_project serialization
2. Fix Bug #2: merge_requests.list_merge_requests serialization
3. Fix Bug #5: pipelines.list_pipelines data structure
4. Fix Bug #3: projects.search_projects parameter
5. Fix Bug #4: repositories.search_code parameter
6. Re-test all 26 tools to verify fixes

### Phase 2: Expand Testing (2 hours)
7. Enhance test script to cover all 79 tools systematically
8. Run comprehensive test suite
9. Document all newly discovered bugs

### Phase 3: Fix Remaining Bugs (2-4 hours)
10. Fix all bugs found in Phase 2
11. Re-run comprehensive tests
12. Achieve 100% pass rate

### Phase 4: Quality Assurance (2 hours)
13. Create automated regression tests
14. Integrate tests into CI/CD pipeline
15. Update all documentation
16. Create usage examples for working tools

---

## Success Criteria

✅ **Phase 1 Complete** when:
- All 5 known bugs are fixed
- All 26 tested tools pass
- Pass rate: 100% of tested tools

✅ **Phase 2 Complete** when:
- Test script covers all 79 tools
- Full test results documented
- All bugs categorized

✅ **Phase 3 Complete** when:
- All 79 tools tested
- All bugs fixed
- Pass rate: 100%

✅ **Phase 4 Complete** when:
- Regression tests in place
- CI/CD pipeline validates all tools
- Documentation accurate and complete

---

## Estimated Total Effort

- **Phase 1**: 1 hour (fix 5 known bugs)
- **Phase 2**: 2 hours (expand testing)
- **Phase 3**: 2-4 hours (fix remaining bugs)
- **Phase 4**: 2 hours (quality & docs)

**Total**: **7-9 hours** to achieve fully working MCP server with 100% pass rate

---

## Test Results File

Detailed JSON results saved to: `mcp_test_results_all_79.json`

---

## Next Steps

1. Begin Phase 1: Fix the 5 critical bugs
2. Create pull request with fixes
3. Run automated tests to verify
4. Proceed to Phase 2: Expand test coverage

---

**Status**: 🔴 IN PROGRESS - Phase 1 Pending
**Last Updated**: 2025-10-24
**Test Coverage**: 33% (26/79 tools)
**Pass Rate**: 80.8% (21/26 tested tools)
**Target**: 100% pass rate across all 79 tools
