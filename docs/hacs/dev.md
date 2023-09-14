### Steps for Adding HACS Integration

#### 1. Prepare your repository

Make sure your GitHub repository meets the following requirements:

- It must contain a `.hacs.json` file with metadata for the HACS frontend. The file should look something like this:

  ```json
  {
    "name": "Renpho Weight Scale Integration",
    "domains": ["sensor"],
    "documentation": "https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/blob/main/README.md",
    "codeowners": ["@YOUR_USERNAME"],
    "icon": "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPOSITORY/main/icon.png",
    "country": ["us"]
  }
  ```

- The repository must contain a `README.md` file.
- You must tag a release. The tag should be a version number and the release should include a changelog.

#### 2. Add Custom Repository to HACS

Before your repository is listed in the HACS default store, users can manually add it to their HACS installation by following these steps:

1. Open Home Assistant and navigate to HACS.
2. Click on "Integrations."
3. Click on the three dots in the top right corner and choose "Custom repositories."
4. Paste the URL of your GitHub repository and select "Integration" as the category.

#### 3. Make a Pull Request to HACS Default Repositories

To make your repository available to everyone by default:

1. Fork the [hacs/default](https://github.com/hacs/default) repository.
2. Add your repository to the `integration` list in the `repositories.json` file.
3. Create a Pull Request.

Your Pull Request will be reviewed, and if it meets the criteria, it will be merged, making your integration available to everyone using HACS by default.

#### 4. Update README

Update your README.md file to include instructions on how to install the component via HACS. You can include a HACS badge to show that it's available through HACS.
