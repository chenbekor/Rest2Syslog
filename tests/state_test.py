from r2s_state import State, DEFAULT_PERSIST_PATH
import os

def setup_function(function):
    try:
        os.remove(DEFAULT_PERSIST_PATH)
    except: pass

def  test_persist():
    state = State(last_record_id='4')
    assert state.last_record_id == '4'

    state.last_record_id = '6'
    state.persist()

    restored_state = State()

    assert restored_state.last_record_id == '6'