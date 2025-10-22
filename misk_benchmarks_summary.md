# Misk Software Engineering Benchmarks - Task Selection Summary

This document provides details about the 10 software engineering tasks curated from the misk open-source repository.

## Selection Criteria

Each task was selected based on:
1. **Well-specified issue or PR description** - Clear problem statement
2. **Fail-to-pass tests** - Tests that fail before the fix and pass after
3. **Real-world applicability** - Actual bugs/issues from production use
4. **Complexity and educational value** - Non-trivial problems requiring understanding of the codebase
5. **Kotlin representation** - All tasks are in Kotlin

## Top 10 Tasks (Ranked)

### 1. Query Pagination Bug (PR #1614)
- **Issue**: #1613 - Pager generates duplicate WHERE conditions and ORDER BY clauses
- **Fix**: Added `clone()` method to Query to prevent mutation of original query
- **Tests**: `RealPagerTest.kt` and `ReflectionQueryFactoryTest.kt` (100 lines added)
- **Complexity**: High - involves query building, pagination, and database operations
- **Why selected**: Complex real-world database pagination bug with comprehensive test coverage

### 2. FakeRedis del() Bug (PR #3449)
- **Issue**: #3411 - FakeRedis.del() only deletes from string store, ignoring other data types
- **Fix**: Modified del() to check and remove keys from all stores (lists, hashes, sorted sets)
- **Tests**: `AbstractRedisTest.kt` (102 lines added)
- **Complexity**: Medium - test infrastructure improvement
- **Why selected**: Clear bug with excellent test coverage demonstrating the fix

### 3. ReflectionQuery Clone Bug (PR #3402)
- **Issue**: #3401 - ReflectionQuery.clone() doesn't clone all fields (maxRows, firstResult)
- **Fix**: Corrected logic to check original object instead of copy for field values
- **Tests**: `ReflectionQueryFactoryTest.kt` (8 lines added)
- **Complexity**: Medium - subtle logic error in clone implementation
- **Why selected**: Subtle bug that requires careful code review to spot

### 4. Resource Loader URL Scheme (PR #343)
- **Issue**: #342 - Should resource paths use URL-like schemes instead of filesystem paths?
- **Fix**: Changed from `/resources/...` to `resources:/...` scheme
- **Tests**: Multiple test files updated (`ResourceLoaderTest.kt` + 7 others, 71 lines total)
- **Complexity**: High - API change affecting many parts of the codebase
- **Why selected**: Well-documented issue with comments, significant refactoring task

### 5. MiskConfig Error Messages (PR #2978)
- **Issue**: Well-specified in PR - NullPointerException for missing fields in config lists
- **Fix**: Use index instead of fieldName for list items in error messages
- **Tests**: `MiskConfigTest.kt` and `TestConfig.kt` (23 lines added)
- **Complexity**: Medium - error handling and configuration parsing
- **Why selected**: Good example of improving developer experience with better error messages

### 6. SQS Consumer Shutdown (PR #2758)
- **Issue**: #2243 - SQS consumers run independently after service shutdown
- **Fix**: Properly stop consumers and executor service during shutdown
- **Tests**: Modified service lifecycle behavior
- **Complexity**: High - concurrency and service lifecycle management
- **Why selected**: Real-world concurrency bug with proper shutdown semantics

### 7. LaunchDarkly Feature Flags Logging (PR #2086)
- **Issue**: #1991 - Adding new fields to JSON feature flags causes errors in logs
- **Fix**: Log unknown fields once at WARN level instead of ERROR for each evaluation
- **Tests**: `LaunchDarklyFeatureFlagsTest.kt` (48 lines added)
- **Complexity**: Medium - feature flag evaluation and logging
- **Why selected**: Practical problem with backward compatibility and logging

### 8. gRPC Error Handling (PR #1983)
- **Issue**: #1933 - Misk throws HTTP status codes for gRPC errors instead of grpc-status header
- **Fix**: Return HTTP 200 with grpc-status header per gRPC spec
- **Tests**: `MiskClientMiskServerTest.kt` and `GrpcConnectivityTest.kt` (64 lines added)
- **Complexity**: High - protocol compliance and error handling
- **Why selected**: Important protocol compliance fix with good test coverage

### 9. FakeJobQueue Deadletter Assertion (PR #2081)
- **Issue**: #2080 - FakeJobQueue asserts deadlettered jobs are acknowledged
- **Fix**: Don't check acknowledgment for deadlettered jobs
- **Tests**: `FakeJobQueueTest.kt` (14 lines added)
- **Complexity**: Low-Medium - test framework behavior
- **Why selected**: Clear issue with test framework improvement

### 10. CoordinatedService Shutdown Deadlock (PR #1976)
- **Issue**: #1975 - Deadlock when shutting down multiple services
- **Fix**: Reverted synchronization lock object change that caused deadlock
- **Tests**: Fixes intermittent test timeouts
- **Complexity**: High - concurrency and deadlock debugging
- **Why selected**: Real-world concurrency bug requiring deadlock analysis

## Task Characteristics

- **Language**: 100% Kotlin
- **Domains**: Database operations, concurrency, testing infrastructure, configuration, protocols
- **Bug Types**: Logic errors, concurrency issues, API design, protocol compliance
- **Test Coverage**: All tasks have associated fail-to-pass tests
- **Issue Quality**: 9 out of 10 have well-specified GitHub issues

## Notes

- All PRs are merged and publicly accessible
- All commits are available in the cashapp/misk repository
- Tests can be run locally to verify fail-to-pass behavior
- Tasks represent real-world problems from a production Kotlin framework
