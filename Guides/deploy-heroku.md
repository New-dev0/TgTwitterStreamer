# Deploy to Heroku

## Deploying through Fork
- [Fork](https://github.com/New-dev0/TgTwitterStreamer/fork) this repository.
- Create an app in your [heroku account](https://dashboard.heroku.com/).
- Connect your Heroku Account to Github Account and heroku app to Github Repository.
- Choose `main` branch and click deploy.
- Done

## Deploying through Heroku-CLI
- Install [Heroku-Cli](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli).
- [Install git](https://git-scm.com/downloads) if you don't have it installed.
- Open `Command Prompt`.
- Run `git clone https://github.com/New-dev0/TgTwitterStreamer`
- Move into directory. (`cd TgTwitterStreamer`)
- Run `heroku create` to create new app (remember the app name for later).
- Create git remote `git remote -v`.
- Run `heroku git:remote -a app_name` (Replace app name by previously created app name).
- Deploy `git push heroku main`
- Done (test your app).