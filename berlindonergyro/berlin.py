#!/usr/bin/python
"""
    ULTIMATE SCRIPT

    It uses data written in files:
        * follow_followers.txt
        * follow_following.txt
        * like_hashtags.txt
        * like_users.txt
    and do the job. This bot can be run 24/7.
"""

import os
import sys
import time
from random import shuffle

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot


bot = Bot(
    max_likes_per_day=1000,
    max_unlikes_per_day=1000,
    max_follows_per_day=350,
    max_unfollows_per_day=350,
    max_comments_per_day=100,
    max_likes_to_like=100,
    max_followers_to_follow=2000,
    min_followers_to_follow=10,
    max_following_to_follow=7500,
    min_following_to_follow=10,
    max_followers_to_following_ratio=10,
    max_following_to_followers_ratio=2,
    min_media_count_to_follow=6,
    like_delay=10,
    unlike_delay=10,
    follow_delay=30,
    unfollow_delay=30,
    comment_delay=60,
    whitelist=None,
    comments_file="comment.txt",
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])


bot.login()

print("Current script's schedule:")
follow_followers_list = bot.read_list_from_file("follow_followers.txt")
print("Going to follow followers of:", follow_followers_list)
follow_following_list = bot.read_list_from_file("follow_following.txt")
print("Going to follow following of:", follow_following_list)
like_hashtags_list = bot.read_list_from_file("hashtagsdb.txt")
print("Going to like hashtags:", like_hashtags_list)
like_users_list = bot.read_list_from_file("like_users.txt")
print("Going to like users:", like_users_list)


tasks_list = []
for item in follow_followers_list:
    tasks_list.append(
        (bot.follow_followers, {'user_id': item, 'nfollows': None}))
for item in follow_following_list:
    tasks_list.append((bot.follow_following, {'user_id': item}))
for item in like_hashtags_list:
    tasks_list.append((bot.like_hashtag, {'hashtag': item, 'amount': None}))
    tasks_list.append(bot.comment_hashtag(item))
for item in like_users_list:
    tasks_list.append((bot.like_user, {'user_id': item, 'amount': None}))
    
tasks_list.append(bot.unfollow_non_followers())

shuffle(tasks_list)
for func, arg in tasks_list:
    func(**arg)
