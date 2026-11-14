import uuid

import pytest

from app.core.errors import InvalidEntryError
from app.services.ledger import Movement, build_entries, validate_movements

def make_ids(n:int)->list[uuid.UUID]:
    return [uuid.uuid4() for _ in range(n)]

def test_validate_movements():
    a,b=make_ids(2)
    validate_movements([Movement(a,b,500)])
    
def test_multiple_movements():
    a,b,c=make_ids(3)
    validate_movements([Movement(a,b,300), Movement(a,c,200)])
    
def test_empty_list():
    with pytest.raises(InvalidEntryError):
        validate_movements([])

@pytest.mark.parametrize("amount",[0,-1,-500])
def test_non_positive_amount_rejected(amount):
    a,b=make_ids(2)
    with pytest.raises(InvalidEntryError):
        validate_movements([Movement(a,b,amount)])

@pytest.mark.parametrize("amount",[10.5,"10",None, True, False])
def test_non_integer_amount_rejected(amount):
    a,b=make_ids(2)
    with pytest.raises(InvalidEntryError):
        validate_movements([Movement(a,b,amount)])
        
def test_self_transfer_rejected():
    a=uuid.uuid4()
    with pytest.raises(InvalidEntryError):
        validate_movements([Movement(a,a,500)])

def test_one_bad_movement_rejects_whole_batch():
    a,b=make_ids(2)
    with pytest.raises(InvalidEntryError):
        validate_movements([Movement(a,b,100),Movement(a,a,10)])

def test_single_movement_makes_two_entries():
    a,b=make_ids(2)
    entries,net=build_entries([Movement(a,b,500)])
    assert entries == [(a,-500),(b,500)]
    assert net == {a:-500, b:500}

def test_entries_always_sum_to_zero():
    a,b,c=make_ids(3)
    entries,net=build_entries([Movement(a,b,250),Movement(b,c,180),Movement(c,a,23)])
    assert sum(amount for _,amount in entries) == 0
    assert sum(net.values()) == 0

def check_chunks_from_same_sender_netted():
    a,b=make_ids(2)
    entries,net=build_entries([Movement(a,b,200),Movement(a,b,300)])
    assert net == {a:-500, b:500}
    
def fee_style_transaction():
    a,b,fees=make_ids(2)
    _,net=build_entries([Movement(a,b,1000),Movement(a,fees,500)])
    assert net == {a:-1500, b:1000 , fees:500}
    
def test_opposite_movements_cancel_out():
    a,b=make_ids(2)
    _,net=build_entries([Movement(a,b,300),Movement(b,a,300)])
    assert net == {a:0, b:0}

def test_topup_shape():
    bank, wallet=make_ids(2)
    _,net=build_entries([Movement(bank,wallet,10000)])
    assert net[bank]==-10000
    assert net[wallet]==10000