default_config = {
    "global": {
        "timezone": "Asia/Shanghai",
        "skip_days": 180,
        "max_events": 20,
        "max_days": 30000,
        "interval": 1000,
        "max_ages": 80,
        "solar_birthday": False,
        "lunar_birthday": True,
        "event_time": "10:00:00",
        "event_hours": 2,
        "reminders": [1, 3],
        "attendees": [],
    },
    "pastebin": {
        "enabled": False,
        "base_url": "https://komj.uk",
        "expiration": "",
        "admin_url": "",
        "suggest_url": "",
    },
    "persons": [],
}

tests_config = {
    "persons": [
        {
            "username": "张三",
            "startdate": "1989-06-03",
            "solar_birthday": False,
            "lunar_birthday": True,
        },
        {
            "username": "李四",
            "startdate": "2006-02-01",
            "solar_birthday": True,
            "lunar_birthday": False,
        },
    ],
}

tests_config_overwride_global = {
    "global": {
        "timezone": "America/Los_Angeles",
    },
    "persons": [
        {
            "username": "张三",
            "startdate": "1989-06-03",
            "solar_birthday": False,
            "lunar_birthday": True,
        },
        {
            "username": "李四",
            "startdate": "2006-02-01",
            "solar_birthday": True,
            "lunar_birthday": False,
        },
    ],
}
