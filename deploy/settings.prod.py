# Add newrelic here since it shouldn't be used on non-production servers
MIDDLEWARE_CLASSES.append('middleware.NewRelic')
NEW_RELIC_TRACKING = True
