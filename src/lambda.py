import json
import os
import requests

def lambda_handler(event, context):
    # search for Jira issues
    jira_response = search_jira_issues()
    total_tasks = jira_response.json()['total']

    notification_message = str(total_tasks) + ' task(s) encontrada(s)'
    for issue in jira_response.json()['issues']:
        notification_message = notification_message + '. Task ' + issue['key'] + ': '
        notification_message = notification_message + os.environ['JIRA_API_BASE_URL'] + '/browse/' + issue['key']

    # send slack notification
    slack_response = send_slack_notification(notification_message)

    return 'ok'

def search_jira_issues():
    jira_api_base_url = os.environ['JIRA_API_BASE_URL']
    jira_issues_jql = 'status IN ("In Progress") AND project = "sample project" order by created DESC'
    jira_search_issues_endpoint = f'{jira_api_base_url}/rest/api/2/search?jql={jira_issues_jql}'

    jira_api_basic_auth_user = os.environ['JIRA_API_BASIC_AUTH_USER']
    jira_api_basic_auth_pass = os.environ['JIRA_API_BASIC_AUTH_PASS']

    return requests.get(jira_search_issues_endpoint, auth=(jira_api_basic_auth_user, jira_api_basic_auth_pass))

def send_slack_notification(message):
    slack_api_base_url = os.environ['SLACK_API_BASE_URL']
    slack_send_message_endpoint = f'{slack_api_base_url}/chat.postMessage'
    slack_auth_token = os.environ['SLACK_API_AUTH_TOKEN']
    slack_headers = {
        'Authorization': f'Bearer {slack_auth_token}'
    }
    slack_post_params = {'channel': 'C02UFTR1Z6Y', 'text': message}

    return requests.post(slack_send_message_endpoint, headers=slack_headers, data=slack_post_params)