import pytest
from auth.user_lockout import logFailedAttempt, isLocked, resetFailedAttempts

pytestmark = pytest.mark.usefixtures("db", "clock")

#Account not locked with no failures
def testNotLockedWithNoFailures(db, clock):
    assert isLocked("user@example.com")[0] is False

#Account not locked with two failures
def testTwoDoesNotLock(db, clock):
    for _ in range(2):
        logFailedAttempt("user@example.com")
    assert isLocked("user@example.com")[0] is False

#Account locked with three failures
def testThreeLocks(db, clock):
    for _ in range(3):
        logFailedAttempt("user@example.com")

    locked, minutes, seconds = isLocked("user@example.com")

    assert locked is True
    assert minutes == 5
    assert seconds == 0

#Account locked inside 300 second window
def testLockedWindow(db, clock):
    for _ in range(3):
        logFailedAttempt("user@example.com")
    clock[0] = 1299.0
    assert isLocked("user@example.com")[0] is True

#Account not locked outside 300 second window
def testOutsideWindow(db, clock):
    for _ in range(3):
        logFailedAttempt("user@example.com")
    clock[0] = 1301.0
    assert isLocked("user@example.com")[0] is False

#Attempt number reset outside of 300 second window
def testAttemptReset(db, clock):
    for _ in range(2):
        logFailedAttempt("user@example.com")
    clock[0] = 1301.0

    logFailedAttempt("user@example.com")
    assert isLocked("user@example.com")[0] is False

#Account locked on boundary of 300 second window
def testBoundaryLockoutTime(db, clock):
    for _ in range(3):
        logFailedAttempt("user@example.com")
    clock[0] = 1300.0

    assert isLocked("user@example.com")[0] is True

#Attempts reset upon success
def testSuccessReset(db, clock):
    for _ in range(2):
        logFailedAttempt("user@example.com")
    resetFailedAttempts("user@example.com")

    logFailedAttempt("user@example.com")
    assert isLocked("user@example.com")[0] is False

#Lockout attempts are independent for each account
def testIndependentLockout(db, clock):
    for _ in range(3):
        logFailedAttempt("a@example.com")

    assert isLocked("b@example.com")[0] is False
