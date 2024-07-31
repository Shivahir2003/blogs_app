from rest_framework.throttling import UserRateThrottle

class CommentsThrottlePerDay(UserRateThrottle):
    scope ='commentsperday'


class CommentsThrottlePerSeconds(UserRateThrottle):
    scope ='commentsperSeconds'