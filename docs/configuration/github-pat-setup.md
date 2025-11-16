# GitHub Personal Access Token Setup Guide

## Introduction
A Personal Access Token (PAT) is a secure way to access your GitHub account from external applications. This guide will walk you through the steps to create a PAT and use it for authentication.

## Creating a Personal Access Token
1. **Log in to GitHub**: Go to [GitHub](https://github.com) and log in to your account.
   
2. **Navigate to Settings**: In the upper-right corner, click on your profile photo, then click **Settings**.
   
3. **Developer settings**: On the left sidebar, click on **Developer settings**.
   
4. **Personal access tokens**: Click on **Personal access tokens** in the left sidebar, then select **Tokens (classic)**.
   
5. **Generate new token**: Click the **Generate new token** button.
   
6. **Fill in details**:
   - **Token description**: Give your token a descriptive name.
   - **Expiration**: Choose an expiration that fits your needs.
   - **Select scopes**: Select the scopes or permissions you'd like to grant this token. For example, to access repositories, select `repo`.
   
7. **Generate token**: Click the **Generate token** button. **Important**: Copy your new personal access token now. You won’t be able to see it again!

## Using Your Personal Access Token
When prompted for your username and password in the command line or in an application using your token, use your GitHub username as the username and the generated token as the password.

## Conclusion
You have now successfully created a Personal Access Token for GitHub. Be sure to keep it secure and never share it publicly.