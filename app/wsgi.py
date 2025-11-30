"""
WSGI entry point for Elastic Beanstalk deployment
"""
import os

# Initialize New Relic before importing the app
if os.environ.get('NEW_RELIC_LICENSE_KEY'):
    import newrelic.agent
    # Try to use config file if it exists, otherwise use environment variables
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'newrelic.ini')
    if os.path.exists(config_file):
        newrelic.agent.initialize(config_file)
    else:
        newrelic.agent.initialize()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
