# CVAT Keypoint Estimation

## Custom CVAT with Pose Estimation

This repository needs to be used in conjunction with [CVAT](https://github.com/cvat-ai/cvat) , adapted to run a custom pose estimation model.
Modifications

This version includes:
    A custom pose estimation model integrated for specific annotation tasks. You'll need to clone the CVAT repo and this repo. In the CVAT repo, you'll see a serverless folder just like in this. Just add this repo's directory to the corresponding directory in CVAT.


## License

The original CVAT code is licensed under the MIT License.
CVAT with Serverless Machine Learning Models

## The steps to deploy CVAT using Nuclio and run a model in CVAT are detailed below:
### **1. Docker Compose to Set Up CVAT**

    docker compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d

*Purpose*: Initializes the CVAT application along with its serverless components.

*Details*:
    
   -  -f docker-compose.yml: Specifies the primary Docker Compose file for the base CVAT setup.
   -  -f components/serverless/docker-compose.serverless.yml: Adds additional configurations to enable serverless functionality in CVAT.
   -  up -d: Starts the defined services in detached mode, allowing them to run in the background.
       
*Outcome*: Both CVAT and its serverless infrastructure are deployed and running as Docker containers.

### **2. Download the Nuclio CLI (nuctl)**

    wget https://github.com/nuclio/nuclio/releases/download/1.13.0/nuctl-1.13.0-linux-amd64

*Purpose*: Downloads the Nuclio command-line interface (CLI), used for managing serverless functions.
    
*Details*:
    - wget: Downloads files from the specified URL.
    - The URL points to the 1.13.0 release of the Nuclio CLI binary for Linux systems.
        
*Outcome*: The nuctl CLI binary is saved to the current directory.

### **3. Make the nuctl Executable**

    sudo chmod +x nuctl-1.13.0-linux-amd64

*Purpose*: Adds executable permissions to the downloaded nuctl binary.
    
*Details*:
    - sudo: Runs the command with administrator privileges to modify file permissions.
    - chmod +x: Adds the executable permission to the file.
            
*Outcome*: The nuctl binary can now be executed from the command line.

### **4. Add nuctl to the System Path**

    sudo ln -sf $(pwd)/nuctl-1.13.0-linux-amd64 /usr/local/bin/nuctl

*Purpose*: Creates a symbolic link to the nuctl binary, making it accessible from anywhere on the system.
    
*Details*:
    - ln -sf: Creates or updates a symbolic link (-s for symbolic and -f to force replacement).
    - $(pwd): Expands to the current working directory where the nuctl binary is located.
    - /usr/local/bin/nuctl: Adds the link to the system’s executable search path.
        
*Outcome*: The nuctl CLI can now be run from any location in the terminal.

### **5. Create a Nuclio Project**

    nuctl create project cvat

*Purpose*: Initializes a new Nuclio project named cvat.
    
*Details*:
    - Projects in Nuclio serve as logical containers for related serverless functions, making it easier to organize and manage them.
        
*Outcome*: A project named cvat is created in Nuclio.

### **6. Create a CVAT Superuser**

    docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'

*Purpose*: Sets up a superuser account for the CVAT web interface, enabling administrative access.

*Details*:
    - docker exec -it: Runs a command interactively inside a running Docker container.
    - cvat_server: Specifies the container name where the command will execute.
    - python3 ~/manage.py createsuperuser: Invokes Django’s built-in management command to create a superuser account. It will prompt you to input details such as a username, email, and password.
    
*Outcome*: A superuser account is created, which can be used to manage CVAT via the web interface.


### **7. Deploy the YOLOv8 Keypoints Model Function**

    sudo nuctl deploy --project-name cvat \--path serverless/pytorch/ultralytics/yolov8-kp/nuclio \--volume `pwd`/serverless/common:/opt/nuclio/common \--platform local


*Purpose*: Deploys the YOLOv8 keypoints detection function as a serverless component under the cvat project.

*Details*:
    - sudo nuctl deploy: Deploys a serverless function to Nuclio.
    - --project-name cvat: Associates the function with the previously created cvat project.
    - --path: Specifies the directory containing the function's configuration, code, and dependencies.
    - --volume: Mounts the local directory serverless/common to /opt/nuclio/common inside the function container. This shared directory may include libraries or configuration files required by the function.
    - --platform local: Specifies that the function will run locally.

*Outcome*: The YOLOv8 function is deployed and ready to process data for keypoint detection.

## Deploying and Checking Model:

At Step 7, we run our desired model which is kept at serverless/pytorch/ultralytics/yolov8-kp folder. After deploying the model run 

    localhost:8080
which will prompt you to authenticate yourself that you add when creating the superuser

### **To use your Model**
 -- Don't Forget to replace the YOUR-MODEL-PATH in main.py if you wish to use this for pose estimation.
1. Create a project where you can chose the model name, and other features
2. In labels, you can add ```from model``` which will give you option to chose from your model and can pick from there
3. Create a new task under the project name
4. Select the AI button in the navigation inside the job
5. use your model, annotate and export it as you required.
