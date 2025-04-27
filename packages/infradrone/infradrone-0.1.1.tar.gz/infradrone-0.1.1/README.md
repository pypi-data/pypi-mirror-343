# InfraDrone 🚀

InfraDrone is a robust infrastructure automation tool designed to simplify the deployment and management of cloud resources, Docker containers, and SSH configurations. With support for multiple cloud providers and a user-friendly terminal interface, InfraDrone empowers developers and DevOps engineers to streamline their workflows.

---

## Features ✨

- **Cloud Infrastructure Deployment**:
  - Supports **Yandex Cloud** and **Google Cloud Platform (GCP)**.
  - Automates VM creation with Terraform templates.
  - Configures SSH access for deployed instances.

- **Docker Management**:
  - Deploys Docker containers with pre-configured templates.
  - Includes support for **Keycloak** and **PostgreSQL**.

- **SSH Configuration**:
  - Manages SSH keys and connections.
  - Automatically updates `ssh.json` for easy access.

- **Extensible Architecture**:
  - Easily add new cloud providers or Docker templates.
  - Modular design for custom workflows.

---

## Project Structure 📂

```plaintext
infradrone/
├── config.py               # Configuration loader and saver
├── deploy.py               # Terminal-based deployment menu
├── infra_operations.py     # Core infrastructure deployment logic
├── menus/                  # Terminal UI menus
│   ├── main_menu.py        # Main menu for navigation
│   ├── ssh_connections.py  # SSH connection management
│   └── deploy_docker.py    # Docker deployment menu
├── tf/                     # Terraform templates for cloud providers
│   ├── gcp/                # GCP-specific templates
│   └── yc/                 # Yandex Cloud-specific templates
├── docker/                 # Docker templates
│   └── ubuntu/keycloak/    # Keycloak Docker setup
├── sh/                     # Shell scripts for installation and helpers
├── utils.py                # Utility functions
├── main.py                 # Entry point for the application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── config.ini              # Configuration file
```

---

## Installation 🛠️

### Prerequisites
- Python 3.10+
- Terraform 0.13+
- Docker and Docker Compose
- Cloud provider credentials (e.g., GCP or Yandex Cloud)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/HMCorp-Fund/infradrone/infradrone.git
   cd infradrone
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the project:
   - Edit `config.ini` to set the `BaseDirectory`:
     ```ini
     [Paths]
     BaseDirectory = %%USERPROFILE%%\infradrone
     ```
   - Add your cloud provider credentials to `config.json`.

4. Run the application:
   ```bash
   python main.py
   ```

---

## Configuration 📄

Before using InfraDrone, you need to configure the project by editing the `config.json` file and ensuring the required keys are in place.

### 1. **Configuring `config.json`**
The `config.json` file contains essential settings for InfraDrone, including SSH credentials, working directories, and cloud provider configurations. Below is an explanation of the key fields:

#### Example `config.json`:
```json
{
    "DEFAULT_SSH_PASSWORD": "admin",
    "DEFAULT_SSH_USER": "admin",
    "WORKING_DIR": "C:\\users\\user\\infradrone\\working_dir",
    "KNOWN_HOSTS_DIR": "~\\.ssh\\known_hosts",
    "SSH_PROVIDER": "gcp",

    "PROVIDERS": {
        "yc": {
            "YC_TOKEN": "your-yandex-cloud-token",
            "YC_CLOUD_ID": "your-cloud-id",
            "YC_FOLDER_ID": "your-folder-id",
            "YC_CLOUD_PREFIX": "your-cloud-prefix",
            "YC_ZONE": "your-zone"
        },
        "gcp": {
            "GCP_CREDENTIALS_FILE": "C:\\users\\user\\infradrone\\keys\\your-gcp-credentials.json",
            "GCP_PROJECT_ID": "your-gcp-project-id",
            "GCP_ZONE": "your-gcp-zone",
            "GCP_VM_ZONE": "your-gcp-vm-zone",
            "GCP_NETWORK": "default",
            "GCP_SUBNET": "default",
            "GCP_SSH_KEY": "C:\\users\\user\\infradrone\\keys\\gcp",
            "GCP_SSH_KEY_PASS": "your-ssh-key-password",
            "GCP_SSH_USER": "your-ssh-username"
        }
    }
}
```

#### Key Fields:
- **`DEFAULT_SSH_USER`** and **`DEFAULT_SSH_PASSWORD`**:
  - Default SSH credentials for connecting to instances.
- **`WORKING_DIR`**:
  - Directory where temporary files and logs will be stored.
- **`KNOWN_HOSTS_DIR`**:
  - Path to the SSH `known_hosts` file.
- **`SSH_PROVIDER`**:
  - The default cloud provider (`gcp` or `yc`).
- **`PROVIDERS`**:
  - Contains provider-specific configurations:
    - **Yandex Cloud (`yc`)**:
      - `YC_TOKEN`: Yandex Cloud API token.
      - `YC_CLOUD_ID` and `YC_FOLDER_ID`: IDs for your Yandex Cloud project.
      - `YC_ZONE`: The zone where instances will be deployed.
    - **Google Cloud Platform (`gcp`)**:
      - `GCP_CREDENTIALS_FILE`: Path to your GCP service account JSON key.
      - `GCP_PROJECT_ID`: Your GCP project ID.
      - `GCP_ZONE` and `GCP_VM_ZONE`: Zones for deploying instances.
      - `GCP_SSH_KEY`: Path to your SSH private key for GCP.
      - `GCP_SSH_USER`: Username for SSH connections.

---

### 2. **Creating an SSH Key**
Before deploying infrastructure, you must create an SSH key pair for secure access to your instances.

#### Steps to Create an SSH Key:
1. Open a terminal or PowerShell.
2. Run the following command to generate an SSH key pair:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
3. Save the key to the specified path (e.g., `C:\users\user\infradrone\keys\gcp`).
4. Add the public key to your cloud provider's metadata:
   - **Google Cloud**: Add the public key to the "SSH Keys" section in the GCP console.
   - **Yandex Cloud**: Add the public key to the "SSH Keys" section in the Yandex Cloud console.

---

### 3. **Creating a Google Cloud Key**
To use InfraDrone with Google Cloud, you need a service account key for authentication.

#### Steps to Create a GCP Service Account Key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin** > **Service Accounts**.
3. Create a new service account or select an existing one.
4. Assign the necessary roles (e.g., `Compute Admin` and `Storage Admin`).
5. Generate a JSON key for the service account:
   - Click **Manage Keys** > **Add Key** > **Create New Key**.
   - Save the JSON key to `C:\users\user\infradrone\keys\your-gcp-credentials.json`.
6. Update the `GCP_CREDENTIALS_FILE` field in `config.json` with the path to this key.

---

## Usage 🚀

### Main Menu
Navigate through the terminal-based menu to deploy infrastructure, manage Docker containers, or configure SSH connections.

### Deploying Cloud Infrastructure
1. Select a cloud provider (e.g., Yandex Cloud or GCP).
2. Choose an OS and a template.
3. Provide instance details (e.g., name, allowed ports).
4. InfraDrone will deploy the instance and configure SSH access.

### Managing Docker Containers
1. Select a Docker OS and template.
2. InfraDrone will deploy the container using `docker-compose`.

### SSH Configuration
- View, add, or delete SSH connections directly from the menu.

---

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.

---

Happy automating! 🎉
