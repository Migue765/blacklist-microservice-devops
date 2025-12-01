"""
WSGI entry point for AWS Elastic Beanstalk deployment
AWS Elastic Beanstalk busca una variable llamada 'application' en este archivo
"""
import os

# Initialize New Relic before importing the app
# Only initialize if not already initialized (e.g., when using newrelic-admin run-program)
if os.environ.get('NEW_RELIC_LICENSE_KEY', '01591B20C0FFADDA87E9C64F9CDD2B757B123ACD84F77EE29BAF5D3FA06B256A'):
    try:
        import newrelic.agent
        from newrelic.api.exceptions import ConfigurationError
        # Try to initialize, but catch ConfigurationError if already initialized
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'newrelic.ini')
            if os.path.exists(config_file):
                newrelic.agent.initialize(config_file)
            else:
                newrelic.agent.initialize()
        except ConfigurationError:
            # Already initialized (e.g., by newrelic-admin run-program), skip
            pass
    except (ImportError, Exception) as e:
        # If New Relic fails to initialize, continue without it
        import sys
        print(f"Warning: New Relic initialization failed: {e}", file=sys.stderr)

from app import create_app

# AWS Elastic Beanstalk espera una variable llamada 'application'
application = create_app()

# Para desarrollo local
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
