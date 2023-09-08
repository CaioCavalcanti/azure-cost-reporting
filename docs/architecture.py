from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import ContainerInstances, ContainerRegistries
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.onprem.client import Users
from diagrams.azure.storage import DataLakeStorage

with Diagram("Azure Cost Reporting", filename="architecture"):
    devs = Users("Developers")

    with Cluster("Azure"):
        cron_job = ContainerInstances("ELT CronJob")
        web_app = ContainerInstances("Web App")
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