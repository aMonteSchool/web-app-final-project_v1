# github-search-behave
WEB UI and API based automation for github user search app based on Behave Python and Selenium

Github User Search is a perfect project to practice API automation and to understand dependency between services and how data is populated on UI. Wep app consumes data directly from Github API

Web App: https://gh-users-search.netlify.app/

API: https://docs.github.com/en/rest/users?apiVersion=2022-11-28

## Installation:
1. clone a repository
2. configure venv and python 3.11
3. install packages: `pip install -r requirements.txt`


## Business Requirements:
As a guest user I assume the story is completed if I am able to search users data such as total user’s number of repositories, followers, following, gists and contact information from GitHub to track the changes in real time.

### Included:
Search can be performed by typing profile name into search field and Enter/Return or clicking on Search button

Search result populates data from Github account corresponding to the search field:
1. User, Followers, Following, Repos and Gists details
2. User component
   - User’s component populates Full Name, Profile, Company Name, Location and Company’s Domain
   - Company’s domain redirects to corresponding url

3. Follow button should redirect to GitHub and reflect the status

4. Followers component
   - Each follower has Name and Link

Not existing user should populate “User does not exist“ message
All data should be updated once changes applied on GitHub app

### Excluded:
Rate limit
