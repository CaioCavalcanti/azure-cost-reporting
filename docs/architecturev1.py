import argparse
from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import ContainerInstances, ContainerRegistries
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.onprem.client import Users
from diagrams.azure.storage import DataLakeStorage

# Define a dictionary to map environment names to web app names
web_app_names = {
    "test": "Web App Test",
    "prod": "Web App Prod",
}

# Define a function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Azure Cost Reporting architecture diagrams")
    parser.add_argument("--environment", required=True, choices=web_app_names.keys(), help="Specify the environment (test or prod)")
    return parser.parse_args()

# Parse the command line arguments
args = parse_arguments()
environment = args.environment

# Use the dictionary to get the web app name
web_app_name = web_app_names[environment]

with Diagram(f"Azure Cost Reporting - {environment}", filename=f"architecture_{environment}"):
    devs = Users("Developers")

    with Cluster("Azure"):
        cron_job = ContainerInstances("ELT CronJob")
        web_app = ContainerInstances(web_app_name)  # Use the customized name here
        storage = DataLakeStorage("Data Lake")
        acr = ContainerRegistries("Container Registry")

    with Cluster("GitHub"):
        git_repo = Github("Git repository")
        ci = GithubActions("CI Pipeline")
        cd = GithubActions("CD Pipeline")

    devs >> Edge(label="Merge PRs into main branch") >> git_repo

    git_repo >> Edge(label="triggers") >> ci

    ci >> Edge(label="1. push image into") >> acr
    ci >> Edge(label="2. trigger") >> cd

    cd >> \
        Edge(label="deploy") >> \
        [web_app, cron_job] >> \
        Edge(label="pull image from") >> \
        acr
    
    cron_job >> Edge(label="read and write") >> storage
    web_app >> Edge(label="read") >> storage
