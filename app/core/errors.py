class LedgerError(Exception):
    """ base class for ledger problems """
    
class InvalidEntryError(LedgerError):
    """Bad entry data: too few entries, zero or non-integer amount, duplicate account."""
    
class UnbalancedEntriesError(LedgerError):
    """Entries in one transaction do not sum to zero."""


class AccountNotFoundError(LedgerError):
    """An entry points at an account that does not exist."""
    
class InsufficientFundsError(LedgerError):
    """Source account balance is lower than the amount."""