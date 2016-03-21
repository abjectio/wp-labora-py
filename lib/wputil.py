"""
:mod:`lib.wputil` -- Library for handling WordPress interaction
==================================================================

.. module:: wputil
   :platform: Unix, Windows
   :synopsis: Library for handling WordPress interaction
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of import_events python code.

import_events is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

import_events is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with import_events.  If not, see <http://www.gnu.org/licenses/>.

"""
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, DeletePost
from lib.util import loginfo, logerror
import sys


def get_wordpress_client(wp_url, wp_user, wp_pwd):
    """Initate a WordPress connection - xmlrpc."""

    #New WordPress object
    loginfo('Initate WordPress client Instance')

    try:
        client = Client(wp_url + '/xmlrpc.php', wp_user, wp_pwd)
        return client
    except IOError as exception:
        logerror(('Could not get wordpress client !! \
         - %s - URL: %s ', exception, wp_url))
        logerror('[EXIT AND ENDS IMPORT]')
        sys.exit(2)


def get_all_ids(client, event_category):
    """Get all WordPressPost IDs of a specific type"""

    #Get all IDs of Posts of post_type 'event'
    loginfo('Get all posts with category-event: [' + \
    event_category + '] and delete those')
    offset = 0
    increment = 10
    ids = []
    while True:
        posts = client.call(GetPosts({'post_type': 'event', 'number': \
        increment, 'offset': offset}))
        if len(posts) == 0:
            break #break no more post
        for one_post in posts:
            if one_post.terms[0].name == event_category:
                ids.append(one_post.id)
        offset += increment
    #Return array of WordPress post IDs
    return ids


def delete_wp_posts(client, ids, dry_run):
    """Delete a range of WordPress posts"""

    #Iterate and delete posts
    for delete_id in ids:
        loginfo('Deleting WordpressPost with ID: [' + delete_id + ']')
        if not dry_run:
            try:
                client.call(DeletePost(delete_id))
            except Exception as e:
                loginfo('Exception deleting post with ID: [' + delete_id + ']' + e)

    loginfo('Finished deleting posts count => ' + ids.count.tostring)




def create_new_wp_post(client, component, event_category, dry_run):
    """Create a new WordPress post"""

    summary = component.get('SUMMARY').encode('UTF-8', 'backslashreplace')
    start_event = component.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M')
    end_event = component.get('DTEND').dt.strftime('%Y-%m-%d %H:%M')
    end_frequency_event = component.get('DTEND').dt.strftime('%Y-%m-%d')
    event_description = component.get('DESCRIPTION').encode('UTF-8', \
    'backslashreplace')


    # Create a new post
    new_post = WordPressPost()
    new_post.title = summary
    new_post.content = event_description
    new_post.post_type = "event"
    new_post.post_status = "publish"
    new_post.terms_names = {'event-category': [event_category]}
    new_post.custom_fields = []

    meta_adds = (['imic_event_start_dt', start_event],
                ['imic_event_end_dt', end_event],
                ['imic_event_frequency_end', end_frequency_event],
                ['imic_featured_event', 'no'],
                ['slide_template', 'default'],
                ['imic_event_day_month', 'first'],
                ['imic_event_week_day', 'sunday'],
                ['imic_event_frequency_type', '0'],
                ['imic_event_frequency', '35'],
                ['imic_event_registration', '0'],
                ['imic_custom_event_registration_target', '0'],
                ['imic_sidebar_columns_layout', '3'],
                ['imic_google_map_track', '1'],
                ['imic_event_address2', 'Tananger kirke, Sola, Norway'],
                ['imic_event_map_location', '58.93535599999999, \
                5.600313000000028'],
                ['imic_pages_banner_overlay', '0'],
                ['imic_pages_banner_animation', '0'],
                ['imic_pages_select_revolution_from_list', '[rev_slider fsl]'],
                ['imic_pages_slider_pagination', 'no'],
                ['imic_pages_slider_auto_slide', 'no'],
                ['imic_pages_slider_direction_arrows', 'no'],
                ['imic_pages_slider_interval', '7000'],
                ['imic_pages_slider_effects', 'fade'],
                ['imic_pages_nivo_effects', 'sliceDown'])

    #Iterate over array creating meta in post
    for i in meta_adds:
        new_post.custom_fields.append({'key':i[0], 'value':i[1]})

    #Add New Post and it's meta data
    loginfo('Create a new WordPressPost - Title: [' + \
    new_post.title + '] Description: [' + \
    new_post.content + '] ' + \
    'Starts: [' + start_event + '] Ends: [' + \
    end_event + ']')
    if not dry_run:
        client.call(NewPost(new_post))


def create_all_posts_from_ical(client, ical, event_category, dry_run):
    """Create new WordPress posts from ICalendar object"""

    i = 0
    for component in ical.walk('VEVENT'):
        create_new_wp_post(client, component, event_category, dry_run)
        i += 1
    loginfo(('Created %s WordPress posts', i))
