# Configure the Netlify Provider
provider "netlify" {
}

data "external" "copilot_deploy" {
    program = [
        "${path.module}/../bin/copilot.sh"
    ]
}

# Create a new deploy key for this specific website
resource "netlify_deploy_key" "key" {}

# Define your site
resource "netlify_site" "web" {
  name = "my-site"

  repo {
    repo_branch   = "main"
    command       = "cd ./fronts/web && yarn build"
    deploy_key_id = "${netlify_deploy_key.key.id}"
    dir           = "./fronts/web/dist"
    provider      = "github"
    repo_path     = "l-monninger/arkham"
  }
}