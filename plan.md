1. **Understand the Testing Gap**: The issue asks for missing error path tests for `gnc_account_set_balance_dirty` in `libgnucash/engine/Account.cpp:1900`.
The `gnc_account_set_balance_dirty` function has two error/early return paths:
  - `g_return_if_fail(GNC_IS_ACCOUNT(acc))`
  - `if (qof_instance_get_destroying(acc))`
2. **Plan**: Write a new test function `test_gnc_account_set_balance_dirty_error_paths` in `libgnucash/engine/test/utest-Account.cpp`.
  - To test `g_return_if_fail(GNC_IS_ACCOUNT(acc))`, we will call `gnc_account_set_balance_dirty(NULL)` and verify that a CRITICAL message is logged using `g_test_expect_message` and `g_test_assert_expected_messages`. We can also use an invalid/non-account pointer but NULL is simplest.
  - To test the `qof_instance_get_destroying(acc)` early return path, we need to set the destroying flag on a dummy account and call the function. Because there is no public getter for `balance_dirty`, we will verify that calling it does not crash or trigger assertions, which covers the execution path (code coverage will hit the `return;` line).
3. **Implement**:
  - Add `static void test_gnc_account_set_balance_dirty_error_paths()` in `utest-Account.cpp`.
  - `g_test_expect_message ("gnc.engine", G_LOG_LEVEL_CRITICAL, "*assertion*GNC_IS_ACCOUNT*");`
  - `gnc_account_set_balance_dirty(NULL);`
  - `g_test_assert_expected_messages();`
  - Create a dummy account.
  - Call `qof_instance_set_destroying(acc, TRUE);`.
  - Call `gnc_account_set_balance_dirty(acc);`.
  - Verify it completes safely.
  - Register the new test function in `test_suite_account()`.
4. **Pre-commit**: Call `pre_commit_instructions` before submitting.
5. **Verify**: Compile and run the test using Ninja. Ensure it passes and increases code coverage.
