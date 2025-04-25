# Task ID: 1
# Title: Fix External Integration Tests
# Status: pending
# Dependencies: 
# Priority: high
# Description: Fix import errors in external integration tests

# Details:
The external integration tests are currently failing due to import errors. The module structure has changed, but the tests haven't been updated to reflect these changes. The following files need to be updated:

1. `test_external_integration.py` - Update import statements to match the current module structure
2. `test_integration_sync.py` - Fix imports for `ExternalSystem`, `SyncStatus`, and `ExternalSyncMetadata`
3. `test_nextcloud_adapter.py` - Fix imports for `ExternalSyncMetadata`
4. `test_sync_manager.py` - Fix imports for `ExternalSyncMetadata`

The current error is that these classes cannot be imported from `taskinator.external_integration`. We need to determine where these classes have been moved to and update the import statements accordingly.

# Test Strategy:
1. Examine the current module structure to identify where the missing classes are now located
2. Update import statements in each test file
3. Run each test file individually to verify the imports are fixed
4. Run the full test suite to ensure no regressions
