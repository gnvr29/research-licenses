# How to use
### Create a GitHub token with the correct permissions:
Login to your Github profile, click on your profile picture on the top-right corner and select settings.

On the settings page, scroll down and click **Developer settings**. Then, click on **Personal access tokens**, and then on **Fine-grained tokens**. 

Click to generate a new token, attributing any name and description you wish. Scroll down, and, on Repository access, select **Only select repositories**. After that, click on Repository access and select the following permissions:
- **Content**: (read-only)
- **Metadata**: (read-only)

After this, click on **Generate token**. Copy and paste it somewhere safe, for you won't be able to see it again.

### Executing the project:

Create a **.env** file in the project root, and add the following variable in there:

- GITHUB_TOKEN=<your-newly-generated-token>
