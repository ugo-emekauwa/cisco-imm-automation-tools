<h1 align="center">Switch Control Policy Maker</h1>

<h1 align="center">
  <img alt="Policy Makers Title Image" title="Policy Makers" src="./assets/Policy_Makers_Title_Graphic.png">
</h1>  

<p align="center">
  The Switch Control Policy Maker for Cisco Intersight automates the creation of Switch Control Policies.
</p>
<br>

## Features
- Automatically build an Intersight Switch Control Policy to your exact specification. Anything that can be done through the Intersight GUI can be done here and more!

- Automatically attach the Switch Control Policy to a UCS Domain Profile if desired, during the Switch Control Policy configuration.

- Supported with Intersight SaaS, Connected Virtual Appliance, and Private Virtual Appliance.

## Prerequisites
1. Python 3 installed, which can be downloaded from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Install the Cisco Intersight SDK for Python by running the following command:
   ```
   python -m pip install git+https://github.com/CiscoUcs/intersight-python.git
   ```
   More information on the Cisco Intersight SDK for Python can be found at [https://github.com/CiscoUcs/intersight-python](https://github.com/CiscoUcs/intersight-python).
3. [_Optional_] If you already have the Cisco Intersight SDK for Python installed, you may need to upgrade. An upgrade can be performed by running the following command:
   ```
   python -m pip install git+https://github.com/CiscoUcs/intersight-python.git --upgrade --user
   ```
4. Clone or download the Cisco IMM Automation Tools repository by using the ![GitHub Code Button](./assets/GitHub_Code_Button.png "GitHub Code Button") link on the main repository web page or by running the following command:
    ```
    git clone https://github.com/ugo-emekauwa/cisco-imm-automation-tools
    ```
5. Generate a version 2 API key from your Intersight account.

    **(a).** Log into your Intersight account, click the Settings icon and select **Settings**.
    
      ![Figure 1 - Go to Settings](./assets/Figure_1_Go_to_Settings.png "Figure 1 - Go to Settings")
      
    **(b).** Under the API section in the work pane, click **API Keys**.
    
      ![Figure 2 - Go to API Keys](./assets/Figure_2_Go_to_API_Keys.png "Figure 2 - Go to API Keys")
      
    **(c).** In the API Keys section in the work pane, click the **Generate API Key** button.
    
      ![Figure 3 - Click the Generate API Key button](./assets/Figure_3_Click_the_Generate_API_Key_button.png "Figure 3 - Click the Generate API Key button")
      
    **(d).** In the Generate API Key window, enter a description or name for your API key.
    
      ![Figure 4 - Enter an API key description](./assets/Figure_4_Enter_an_API_key_description.png "Figure 4 - Enter an API key description")
      
    **(e).** In the Generate API Key window, under API Key Purpose, verify a version 2 API key is selected.
    
      ![Figure 5 - Verify version 2 API key selection](./assets/Figure_5_Verify_version_2_API_key_selection.png "Figure 5 - Verify version 2 API key selection")
      
    **(f).** In the Generate API Key window, click the **Generate** button.
    
      ![Figure 6 - Click the Generate button](./assets/Figure_6_Click_the_Generate_button.png "Figure 6 - Click the Generate button")
      
    **(g).** In the Generate API Key window, a new API key will be generated. Copy the API Key ID and download the Secret Key to a secure location.
    
      ![Figure 7 - Copy and save the API key data](./assets/Figure_7_Copy_and_save_the_API_key_data.png "Figure 7 - Copy and save the API key data")

## How to Use
1. Please ensure that the above [**Prerequisites**](https://github.com/ugo-emekauwa/cisco-imm-automation-tools#prerequisites) have been met.
2. Within the Cisco IMM Automation Tools repository, navigate to the folder \src\policy_makers\switch_control_policy_maker.
3. Edit the switch_control_policy_maker.py file to set the **`key_id`** variable using the following instructions:

    **(a).** Open the switch_control_policy_maker.py file in an IDLE or text editor of choice.
    
    **(b).** Find the comment **`# MODULE REQUIREMENT 1 #`**.
     
      ![Figure 9 - MODULE REQUIREMENT 1 location](./assets/Figure_9_MODULE_REQUIREMENT_1_location.png "Figure 9 - MODULE REQUIREMENT 1 location")
      
    **(c).** Underneath, you will find the variable **`key_id`**. The variable is currently empty.
    
      ![Figure 10 - key_id variable location](./assets/Figure_10_key_id_variable_location.png "Figure 10 - key_id variable location")
      
    **(d).** Fill in between the quotes of the **`key_id`** variable value with the ID of your API key. For example:
      ```py
      key_id = "5c89885075646127773ec143/5c82fc477577712d3088eb2f/5c8987b17577712d302eaaff"
      ```
3. Edit the switch_control_policy_maker.py file to set the **`key`** variable using the following instructions:

    **(a).** Open the switch_control_policy_maker.py file in an IDLE or text editor of choice.
    
    **(b).** Find the comment **`# MODULE REQUIREMENT 2 #`**.
    
      ![Figure 11 - MODULE REQUIREMENT 2 location](./assets/Figure_11_MODULE_REQUIREMENT_2_location.png "Figure 11 - MODULE REQUIREMENT 2 location")
      
    **(c).** Underneath, you will find the variable **`key`**. The variable is currently empty.
    
      ![Figure 12 - key variable location](./assets/Figure_12_key_variable_location.png "Figure 12 - key variable location")
      
    **(d).** Fill in between the quotes of the **`key`** variable value with your system's file path to the SecretKey.txt file for your API key. For example:
      ```py
      key = "C:\\Keys\\Key1\\SecretKey.txt"
      ```
4. Edit the switch_control_policy_maker.py file to set all the configuration variable values using the following instructions:

    **(a).** Open the switch_control_policy_maker.py file in an IDLE or text editor of choice.

    **(b).** Find the comment **`# MODULE REQUIREMENT 3 #`**.
    
      ![Figure 13 - MODULE REQUIREMENT 3 location](./assets/Figure_13_MODULE_REQUIREMENT_3_location.png "Figure 13 - MODULE REQUIREMENT 3 location")
      
    **(c).** Underneath, you will find the instructions to edit the configuration variable values to match your environment. Each variable has a sample value for ease of use. The variable values to edit begin under the comment **`####### Start Configuration Settings - Provide values for the variables listed below. #######`**.
      
      ![Figure 14 - Start Configuration Settings location](./assets/Figure_14_Start_Configuration_Settings_location.png "Figure 14 - Start Configuration Settings location")
   
    Completion of editing the configuration variable values is marked by the comment **`####### Finish Configuration Settings - The required value entries are complete. #######`**.
      
      ![Figure 15 - Finish Configuration Settings location](./assets/Figure_15_Finish_Configuration_Settings_location.png "Figure 15 - Finish Configuration Settings location")
5. Save the changes you have made to the switch_control_policy_maker.py file.
6. Run the switch_control_policy_maker.py file.

## Where to Demo
The Switch Control Policy Maker can be demoed on Cisco dCloud in the following content:

1. [**_Getting Started with Cisco Intersight v2_**](https://dcloud2-rtp.cisco.com/content/instantdemo/getting-started-with-cisco-intersight-v2)
    - **`NOTE:`** Before running the Switch Control Policy Maker, change the Policy organization to "Sandpit".
2. **_Cisco UCS X-Series with Intersight v1 (Instant Demo)_** - Coming soon!
3. **_Cisco UCS X-Series with Intersight Lab v1 (Scheduled Demo/Sandbox)_** - Coming soon!

dCloud is available at [https://dcloud.cisco.com](https://dcloud.cisco.com), where Cisco product demonstrations and labs can be found in the Catalog.

## Author
Ugo Emekauwa

## Contact Information
uemekauw@cisco.com or uemekauwa@gmail.com
