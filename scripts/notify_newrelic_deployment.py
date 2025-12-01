#!/usr/bin/env python3
"""
Script para notificar a New Relic sobre un nuevo despliegue.
Se ejecuta automáticamente después de cada despliegue en Heroku.
"""
import os
import sys
import requests
import json
from datetime import datetime

def get_deployment_info():
    """Obtener información del despliegue desde variables de entorno"""
    # Priorizar variables de CodeBuild/CodePipeline, luego Heroku, luego defaults
    revision = (
        os.environ.get('CODEBUILD_RESOLVED_SOURCE_VERSION') or
        os.environ.get('CODEBUILD_SOURCE_VERSION') or
        os.environ.get('HEROKU_SLUG_COMMIT') or
        os.environ.get('SOURCE_VERSION', 'unknown')
    )
    
    # Obtener commit hash corto
    if len(revision) > 7:
        revision = revision[:7]
    
    return {
        'revision': revision,
        'description': (
            os.environ.get('CODEBUILD_BUILD_ID') or
            os.environ.get('HEROKU_SLUG_DESCRIPTION') or
            f"Deployment from CodePipeline - Build {os.environ.get('CODEBUILD_BUILD_ID', 'unknown')}"
        ),
        'user': (
            os.environ.get('CODEBUILD_INITIATOR') or
            os.environ.get('HEROKU_USER') or
            os.environ.get('USER', 'unknown')
        ),
        'app_name': os.environ.get('NEW_RELIC_APP_NAME', 'blacklist-microservice'),
        'dyno': os.environ.get('DYNO', 'unknown'),
        'build_id': os.environ.get('CODEBUILD_BUILD_ID', 'unknown'),
    }

def notify_newrelic_deployment():
    """Enviar evento de despliegue a New Relic"""
    
    # Obtener configuración de New Relic
    api_key = os.environ.get('NEW_RELIC_API_KEY')
    license_key = os.environ.get('NEW_RELIC_LICENSE_KEY')
    app_name = os.environ.get('NEW_RELIC_APP_NAME', os.environ.get('HEROKU_APP_NAME', 'blacklist-api'))
    
    if not api_key and not license_key:
        print("Warning: NEW_RELIC_API_KEY or NEW_RELIC_LICENSE_KEY not set. Skipping deployment notification.")
        print("To enable deployment tracking, set NEW_RELIC_API_KEY or NEW_RELIC_LICENSE_KEY environment variable.")
        return False
    
    # Obtener información del despliegue
    deployment_info = get_deployment_info()
    
    success = False
    
    # Método 1: Usar API REST de New Relic (preferido si tenemos API key)
    if api_key:
        try:
            # Obtener el application ID
            apps_url = "https://api.newrelic.com/v2/applications.json"
            headers = {
                'Api-Key': api_key,
                'Content-Type': 'application/json'
            }
            
            apps_response = requests.get(apps_url, headers=headers, timeout=10)
            if apps_response.status_code == 200:
                apps = apps_response.json().get('applications', [])
                app = next((a for a in apps if a['name'] == app_name), None)
                
                if app:
                    app_id = app['id']
                    url = f"https://api.newrelic.com/v2/applications/{app_id}/deployments.json"
                    
                    payload = {
                        'deployment': {
                            'revision': deployment_info['revision'][:40],
                            'changelog': deployment_info['description'],
                            'description': f"Deployment by {deployment_info['user']}",
                            'user': deployment_info['user']
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=payload, timeout=10)
                    if response.status_code in [200, 201]:
                        print(f"✓ Deployment notification sent to New Relic successfully")
                        print(f"  App: {app_name} (ID: {app_id})")
                        print(f"  Revision: {deployment_info['revision']}")
                        success = True
                    else:
                        print(f"Warning: Failed to send deployment notification. Status: {response.status_code}")
                        print(f"Response: {response.text}")
                else:
                    print(f"Warning: Application '{app_name}' not found in New Relic")
                    print("Available applications:")
                    for a in apps[:5]:  # Mostrar solo los primeros 5
                        print(f"  - {a['name']}")
            else:
                print(f"Warning: Failed to fetch applications. Status: {apps_response.status_code}")
        except Exception as e:
            print(f"Error sending deployment notification via API: {e}")
            if not license_key:
                print("No license key available for fallback method.")
    
    # Método alternativo: Usar eventos personalizados vía API de logs (si el método 1 falló o no hay API key)
    if not success and license_key:
        try:
            # Enviar como evento personalizado usando la API de logs
            log_url = "https://log-api.newrelic.com/log/v1"
            headers = {
                'Api-Key': license_key,
                'Content-Type': 'application/json'
            }
            
            log_payload = {
                'timestamp': int(datetime.utcnow().timestamp() * 1000),
                'message': f"Deployment: {deployment_info['revision']}",
                'level': 'INFO',
                'attributes': {
                    'eventType': 'Deployment',
                    'revision': deployment_info['revision'],
                    'description': deployment_info['description'],
                    'user': deployment_info['user'],
                    'app_name': app_name,
                    'dyno': deployment_info['dyno'],
                    'deployment.timestamp': datetime.utcnow().isoformat() + 'Z'
                }
            }
            
            response = requests.post(log_url, headers=headers, json=[log_payload], timeout=10)
            if response.status_code in [200, 202]:
                print(f"✓ Deployment event sent to New Relic via Log API")
                print(f"  App: {app_name}")
                print(f"  Revision: {deployment_info['revision']}")
                success = True
            else:
                print(f"Warning: Failed to send deployment event. Status: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error sending deployment event: {e}")
    
    return success

if __name__ == '__main__':
    success = notify_newrelic_deployment()
    sys.exit(0 if success else 1)

