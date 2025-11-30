"""
WSGI entry point for AWS Elastic Beanstalk deployment
AWS Elastic Beanstalk busca una variable llamada 'application' en este archivo
"""
import os

# Initialize New Relic before importing the app
if os.environ.get('NEW_RELIC_LICENSE_KEY'):
    import newrelic.agent
    # Try to use config file if it exists, otherwise use environment variables
    config_file = os.path.join(os.path.dirname(__file__), 'newrelic.ini')
    if os.path.exists(config_file):
        newrelic.agent.initialize(config_file)
    else:
        newrelic.agent.initialize()

from app import create_app

# AWS Elastic Beanstalk espera una variable llamada 'application'
application = create_app()

# Para desarrollo local
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
