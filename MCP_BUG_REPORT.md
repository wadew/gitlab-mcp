# MCP Server Bug Report - Live Testing Results

**Date**: 2025-10-24
**Test Method**: Live testing against production GitLab instance (gitlab.prod.thezephyrco.com)
**Test Project**: mcps/gitlab_mcp (ID: 22)

## Executive Summary

Out of 11 tools tested, **5 tools are broken (45% failure rate)**. The bugs fall into three categories:
1. **Serialization errors** - Python objects not converted to JSON
2. **Data structure mismatches** - Tools expect lists but get dicts
3. **Parameter name mismatches** - Tool parameters don't match client methods

## Test Results

### ✅ Working Tools (6/11)

1. **list_projects** - Returns project list correctly
2. **list_project_members** - Returns member list (empty but valid)
3. **get_project_statistics** - Returns statistics correctly
4. **list_repository_tree** - Returns directory tree correctly
5. **get_file_contents** - Returns file content correctly
6. **list_issues** - Returns issue list correctly
7. **get_issue** - Returns single issue correctly

### ❌ Broken Tools (5/11)

#### 1. `get_project`
**Error**: `Object of type Project is not JSON serializable`

**Root Cause**: The client returns a python-gitlab `Project` object directly without converting to dict.

**Location**: `src/gitlab_mcp/client/gitlab_client.py` - get_project method needs to call `.asdict()` on the Project object.

**Fix Required**:
```python
# Current (broken):
return project

# Should be:
return project.asdict()
```

---

#### 2. `search_projects`
**Error**: `search_projects() got an unexpected keyword argument 'search'`

**Root Cause**: Parameter name mismatch between MCP tool definition and client method signature.

**Location**: Either:
- Tool is calling with `search=` but client expects different parameter name
- OR client method signature doesn't match tool expectations

**Fix Required**: Align parameter names between tool interface and client implementation.

---

#### 3. `search_code`
**Error**: `search_code() got an unexpected keyword argument 'search'`

**Root Cause**: Same as search_projects - parameter name mismatch.

**Location**: Tool/client parameter name inconsistency.

**Fix Required**: Align parameter names between tool interface and client implementation.

---

#### 4. `list_merge_requests`
**Error**: `Object of type ProjectMergeRequest is not JSON serializable`

**Root Cause**: Same pattern as get_project - returns python-gitlab objects without serialization.

**Location**: `src/gitlab_mcp/client/gitlab_client.py` - list_merge_requests method needs to serialize MR objects.

**Fix Required**: Convert ProjectMergeRequest objects to dicts using `.asdict()` before returning.

---

#### 5. `list_pipelines`
**Error**: `string indices must be integers, not 'str'`

**Root Cause**: **DATA STRUCTURE MISMATCH**
- Client returns: `{"pipelines": [...]}`  (a dict)
- Tool expects: `[...]` (a list)
- Tool iterates over the dict, which gives strings (keys), not pipeline objects

**Location**:
- Client: `src/gitlab_mcp/client/gitlab_client.py:3870` returns `{"pipelines": pipeline_list}`
- Tool: `src/gitlab_mcp/tools/pipelines.py:44-53` tries to iterate directly

**Code Issue**:
```python
# In tools/pipelines.py line 44-53:
pipelines = client.list_pipelines(...)  # Gets {"pipelines": [...]}

# BUG: Iterating over dict gives keys (strings), not values
for pipeline in pipelines:
    formatted_pipelines.append({
        "id": pipeline["id"],  # Tries pipeline["id"] on a STRING!
        ...
    })
```

**Fix Required**:
```python
# Option 1: Fix the tool to access the nested list
result = client.list_pipelines(...)
for pipeline in result["pipelines"]:  # Access the list inside the dict
    ...

# Option 2: Fix the client to return list directly (breaking change)
return pipeline_list  # Instead of {"pipelines": pipeline_list}
```

---

## Bug Categories

### Category A: Serialization Failures (2 bugs)
- `get_project`
- `list_merge_requests`

**Pattern**: Client returns python-gitlab objects without calling `.asdict()`

**Systematic Fix**: Search for all client methods that return gitlab objects and ensure they're serialized.

### Category B: Data Structure Mismatches (1 bug)
- `list_pipelines`

**Pattern**: Client wraps results in dict, but tool expects unwrapped list.

**Systematic Fix**: Audit all client methods for consistent return types. Decide on a standard:
- Always return raw data (lists/dicts)?
- Always wrap in response envelope?

### Category C: Parameter Name Mismatches (2 bugs)
- `search_projects`
- `search_code`

**Pattern**: Tool parameter names don't match client method signatures.

**Systematic Fix**: Create interface validation or use TypedDict/Protocol to ensure consistency.

---

## Impact Assessment

**Severity**: HIGH

- **45% of tested tools are broken**
- Tools that ARE working suggest the architecture can work
- Bugs are systematic - fixing one pattern fixes multiple tools
- Server has been deployed and connected but is unreliable

**User Impact**:
- Cannot reliably use server for GitLab automation
- Documentation (skill file) is misleading - shows tools that don't work
- CI/CD automation would fail if relying on these tools

---

## Recommendations

### Immediate Actions (Priority 1)

1. **Fix Category A (Serialization)** - Highest priority
   - Search all client methods for `return project` or `return merge_request`
   - Add `.asdict()` conversion before returning
   - Estimated: 2-3 hours

2. **Fix Category B (Data Structures)** - High priority
   - Audit client return types for consistency
   - Fix `list_pipelines` tool to match client's dict structure
   - OR change client to return consistent unwrapped data
   - Estimated: 1-2 hours

3. **Fix Category C (Parameters)** - Medium priority
   - Find parameter name mismatches
   - Align tool interfaces with client signatures
   - Estimated: 1 hour

### Short-term Actions (Priority 2)

4. **Create Integration Test Suite**
   - Automate this live testing process
   - Test against real GitLab instance
   - Run before each release
   - Estimated: 4-6 hours

5. **Audit Remaining Tools**
   - Test all 67 tools systematically
   - Document working vs broken
   - Estimated: 3-4 hours

### Long-term Actions (Priority 3)

6. **Add Type Checking**
   - Use Protocols or TypedDict for tool interfaces
   - Validate client method signatures match tool expectations
   - Estimated: 6-8 hours

7. **Standardize Return Types**
   - Decide on consistent data envelope format
   - Document in architecture docs
   - Refactor all client methods
   - Estimated: 8-12 hours

---

## Testing Methodology

### What Worked Well
- Live testing against real instance caught bugs immediately
- Using actual project data provided realistic test cases
- Systematic category-by-category testing

### What Could Improve
- Automated test suite would catch these before deployment
- Type checking would prevent parameter mismatches
- Schema validation would catch serialization issues

---

## Next Steps

1. ✅ Complete testing of all tool categories (DONE)
2. ✅ Document all failures (DONE - this document)
3. ⏳ Fix Category A bugs (serialization)
4. ⏳ Fix Category B bugs (data structures)
5. ⏳ Fix Category C bugs (parameters)
6. ⏳ Re-test all fixed tools
7. ⏳ Create regression test suite
8. ⏳ Update documentation to reflect working state

---

**Prepared by**: Claude Code (automated testing)
**Review Status**: Awaiting human review and prioritization
**Estimated Fix Time**: 4-6 hours for all critical bugs
