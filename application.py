"""
WSGI entry point for AWS Elastic Beanstalk deployment
AWS Elastic Beanstalk busca una variable llamada 'application' en este archivo
"""
from app import create_app

# AWS Elastic Beanstalk espera una variable llamada 'application'
application = create_app()

# Para desarrollo local
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5002, debug=True)
