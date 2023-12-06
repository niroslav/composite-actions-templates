## DevOps-GitHub-Templates
  1. Templates repository checkout **(‼️ Mandatory)**.
  2. Semantic versioning (CI).
  3. Docker build (CI).
  4. Npm test & code coverage (CI).
  5. Dotnet test & code coverage (CI).
  6. Helm chart deployment (CD).
---
#### 1. Templates repository checkout (‼️ Mandatory):
  - Action:
  
    ```
    - name: Checkout DevOps-Templates Repository
      uses: actions/checkout@v3
      with:
        repository: EitanMedical/DevOps-GitHub-Templates
        token: ${{ secrets.CLONE_GITHUB_TOKEN }}
        path: './templates-repo'
        ref: main
    ```
---
#### 2. Semantic Versioning:
  - Action:
    ```
    - name: Run Composite Actions 'semantic-version'
      id: 'sem-ver'
      uses: './templates-repo/.github/templates/semantic-version'
      with:
        templates-workspace: './templates-repo/.github/templates/semantic-version'
    ```
    ---
- Prerequisites (‼️ Mandatory):
  - Checkout
 
    ```
    - name: Checkout
      uses: actions/checkout@v3
      with:
        fetch-depth: 0
    ```
    ---
  - Github repository --> Settings --> Pull Requests
    - Disable "Allow merge commits"
      
    ![image](https://user-images.githubusercontent.com/118258014/229424139-bd1a10be-c2f5-405e-b52e-d70117270b34.png)
    
  ---
- Outputs:
  - For current job:
     ```
     ${{ steps.sem-ver.outputs.shortVersion }} // {major}.{minor}.{patch}                 --> For example: 1.2.3
     ${{ steps.sem-ver.outputs.fullVersion }}  // {major}.{minor}.{patch}.{branch_name}-d --> For example: 1.2.3.fb-d
     ```
     ---
  - For next job:
  
    - Add the following to your current job (where sematic-versioning task is located):
    
      ```
      outputs:
        SHORT_VERSION: ${{ steps.sem-ver.outputs.shortVersion }}
        FULL_VERSION: ${{ steps.sem-ver.outputs.fullVersion }}
      ```
      ---
    - Add the following to your next job:
    
      ```
      needs: {previous_job_name}
      
      env:
        SHORT_VERSION: ${{ needs.{previous_job_name}.outputs.SHORT_VERSION }}
        FULL_VERSION: ${{ needs.{previous_job_name}.outputs.FULL_VERSION }}
        
      steps:
      
        - name: Print New Version
          run : |
            echo ${{ env.SHORT_VERSION }}
            echo ${{ env.FULL_VERSION }}
      ```
---
#### 3. Docker Build:
  - Action:
    ```
    - name: Run Composite Actions 'docker-build'
      uses: "./templates-repo/.github/templates/docker/docker-build"
      with:
        registry: ${{ secrets.ACR_ENDPOINT }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
        version: ${{ steps.sem-ver.outputs.version }}
        file: './DevOps/Dockerfile'
        app: ${{ env.APP }}
        owner: ${{ env.OWNER }}
    ```
    ---
  - Optional:
  
    ```
        context:    'Builds context is the set of files located in the specified PATH or URL (default Git context)'
        build-args: 'List of docker variables'
    ```
---    
#### 4. Npm Test & Code Coverage:
  - Action:
  
    ```
    - name: Run Composite Actions 'npm-test-coverage'
      uses: "./templates-repo/.github/templates/npm-test-coverage"
    ```
---    
#### 5. Dotnet Test & Code Coverage:
  - Action:
  
    ```
    - name: Run Composite Actions 'dotnet-test-coverage'
      uses: "./templates-repo/.github/templates/dotnet-test-coverage"
    ```
---
#### 6. Helm chart deployment:
  - Action:
    
    ```
    - name: Run Composite Actions 'helm-deploy'
      uses: "./templates-repo/.github/templates/chart/helm-deploy"
      with:
        app: ${{ env.APP }}
        owner: ${{ env.OWNER }}
        version: ${{ env.VERSION }}
        key_vault: ${{ env.KEY_VAULT }}
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS }}
        registry: ${{ secrets.ACR_ENDPOINT }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
      env:
        VERSION: ${{ needs.Docker-Build-CI.outputs.VERSION }}
    ```
    ---
  - Optional:
  
    ```
        argocd_deploy_branch: 'The branch from which Argo-CD will deploy. (Default: dev)'
    ```
