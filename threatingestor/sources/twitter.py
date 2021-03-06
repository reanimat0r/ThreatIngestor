from __future__ import absolute_import

import twitter

from threatingestor.sources import Source


TWEET_URL = 'https://twitter.com/{user}/status/{id}'


class Plugin(Source):

    def __init__(self, name, token, token_key, con_secret_key, con_secret, defanged_only=True, **kwargs):
        self.name = name
        self.api = twitter.Twitter(auth=twitter.OAuth(token, token_key, con_secret, con_secret_key))

        # let the user decide whether to include non-obfuscated URLs or not.
        self.include_nonobfuscated = not defanged_only

        # forward kwargs.
        # NOTE: no validation is done here, so if the config is wrong, expect bad results.
        self.kwargs = kwargs

        # decide which endpoint to use based on passed arguments.
        # if slug and owner_screen_name, use List API.
        # if screen_name or user_id, use User Timeline API.
        # if q is set, use Search API.
        # otherwise, default to mentions API.
        self.endpoint = self.api.statuses.mentions_timeline
        if kwargs.get('slug') and kwargs.get('owner_screen_name'):
            self.endpoint = self.api.lists.statuses
        elif kwargs.get('screen_name') or kwargs.get('user_id'):
            self.endpoint = self.api.statuses.user_timeline
        elif kwargs.get('q'):
            self.endpoint = self.api.search.tweets

    def run(self, saved_state):

        # modify kwargs to insert since_id
        if saved_state:
            self.kwargs['since_id'] = saved_state

        # pull new tweets
        response = self.endpoint(**self.kwargs)
        # correctly handle responses from different endpoints
        try:
            tweet_list = response['statuses']
        except TypeError:
            tweet_list = response

        tweets = [{
            'content': s['text'],
            'id': s['id_str'],
            'user': s['user']['screen_name'],
            'entities': s.get('entities', {}),
        } for s in tweet_list]

        artifacts = []
        # traverse in reverse, old to new
        tweets.reverse()
        for tweet in tweets:
            # expand t.co links
            for url in tweet['entities'].get('urls', []):
                try:
                    tweet['content'] = tweet['content'].replace(url['url'], url['expanded_url'])
                except KeyError:
                    # no url/expanded_url, continue without expanding
                    pass

            # process tweet
            saved_state = tweet['id']
            artifacts += self.process_element(tweet['content'],
                                              TWEET_URL.format(user=tweet['user'], id=tweet['id']),
                                              include_nonobfuscated=self.include_nonobfuscated)

        return saved_state, artifacts
