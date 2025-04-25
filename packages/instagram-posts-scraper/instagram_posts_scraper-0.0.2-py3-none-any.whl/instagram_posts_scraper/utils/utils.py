# -*- coding: utf-8 -*-
import concurrent.futures as futures
from datetime import datetime
import pytz
import pandas as pd
from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def timeout(timelimit):
    def decorator(func):
        def decorated(*args, **kwargs):
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    print('Time out!')
                    raise TimeoutError from None
                else:
                    print(result)
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result
        return decorated
    return decorator

def get_current_time(timezone="Asia/Taipei"):
    current_time_utc = datetime.utcnow()
    target_timezone = pytz.timezone(timezone)
    target_current_time = current_time_utc.replace(
        tzinfo=pytz.utc).astimezone(target_timezone)
    return target_current_time

def get_account_status(userid, profile_soup=None):
    if userid == "":
        return "missing"
    else:
        private_span = profile_soup.find(
            "span", class_="ident private icon icon_lock")
        if private_span:
            return "private"
        return "public"

def has_all_data_been_collected(scraped_items:pd.DataFrame,counts_of_posts):
    """Whether program get all posts already."""
    if len(set([each["shortcode"] for each in scraped_items])) >= int(counts_of_posts):
        return True
    return False

def is_date_exceed_half_year(scraped_items:pd.DataFrame, days_limit:int):
    """Check if scraped posts' published date exceed half year"""
    current_time = datetime.now()
    days_ago_list = [int(
        (current_time - pd.to_datetime(each["time"], unit="s")).days) for each in scraped_items]
    
    max_days_ago = max(days_ago_list) # 爬到的貼文裡, 發文時間距離當前時間最遠的日期
    if max_days_ago > days_limit:  # 半年內
        return True
    return False
