from lib.manage_service.timer_map import TimerMap

def test_deserialize():
    tm = TimerMap()
    tm.deserialize()
    print(tm.json_return())

def test_serialize():
    tm = TimerMap()
    tm.serialize()

def test_add_key():
    tm = TimerMap()
    tm.new_timer_key("sample_text")
    tm.serialize()

def test_add_exec_time_value():
    tm = TimerMap()
    tm.new_timer_key("sample_text")
    tm.new_exec_time_value("sample_text", ["He", "*-*-* *:*:0/5", "Mon 15:00:00", "2023-12-31 18:30:00"])

    tm.new_timer_key("He,He")
    tm.new_exec_time_value("He,He", ["He", "2023-12-31 18:30:00", "Tue 18:59:59", "*-*-* *:*:0/5", "2023-12-30 18:30:00"])

    tm.serialize()

test_deserialize()
