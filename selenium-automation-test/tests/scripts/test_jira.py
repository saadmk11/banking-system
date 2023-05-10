import pytest

from jira import JIRA

@pytest.fixture(scope="session")
def jira(request):
    jira_options = {'server': 'https://pccwmmu999.atlassian.net/'}
    jira = JIRA(options=jira_options, basic_auth=('1171201847@student.mmu.edu.my', 'cap^a5cgIty'))
    
    return jira

def test_fetch_jira_issue(jira):
    issue = jira.issue('AT-1')
    assert issue is not None