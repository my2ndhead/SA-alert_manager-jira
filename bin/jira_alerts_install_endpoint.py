import splunk
import splunk.admin as admin
from jira_helpers import *

PASSWORD_PLACEHOLDER = '*******'
DEFAULT_SETTINGS = ('project_key', 'issue_type', 'priority', 'assignee', 'servicedesk_id', 'requesttype_id')

class JiraAlertsInstallHandler(admin.MConfigHandler):
    def __init__(self, *args):
        admin.MConfigHandler.__init__(self, *args)
        self.shouldAutoList = False

    def setup(self):
        self.supportedArgs.addOptArg('*')

    def handleList(self, confInfo):
        jira_settings = get_jira_settings(splunk.getLocalServerInfo(), self.getSessionKey())
        item = confInfo['alert_manager-jira']
        item['jira_url'] = jira_settings.get('jira_url', 'http://your.server/')
        item['jira_username'] = jira_settings.get('jira_username')
        item['jira_password'] = PASSWORD_PLACEHOLDER
        item['jira_servicedesk_mode'] = jira_settings.get('jira_servicedesk_mode')
        for k in DEFAULT_SETTINGS:
            item['default_' + k] = jira_settings.get(k, '')

    def handleEdit(self, confInfo):
        if self.callerArgs.id == 'alert_manager-jira':
            jira_settings = get_jira_settings(splunk.getLocalServerInfo(), self.getSessionKey())
            if 'jira_url' in self.callerArgs:
                jira_settings['jira_url'] = self.callerArgs['jira_url'][0]
            if 'jira_username' in self.callerArgs:
                jira_settings['jira_username'] = self.callerArgs['jira_username'][0]
            if 'jira_password' in self.callerArgs:
                password = self.callerArgs['jira_password'][0]
                if password and password != PASSWORD_PLACEHOLDER:
                    jira_settings['jira_password'] = password
            if 'jira_servicedesk_mode' in self.callerArgs:
                jira_settings['jira_servicedesk_mode'] = self.callerArgs['jira_servicedesk_mode'][0]        
            for k in DEFAULT_SETTINGS:
                if 'default_' + k in self.callerArgs:
                    jira_settings[k] = self.callerArgs['default_' + k][0]
            if not validate_jira_settings(jira_settings):
                raise admin.ArgValidationException, "Error connecting to JIRA server"
            update_jira_settings(jira_settings, splunk.getLocalServerInfo(), self.getSessionKey())

admin.init(JiraAlertsInstallHandler, admin.CONTEXT_APP_ONLY)
