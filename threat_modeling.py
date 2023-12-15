from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
import gradio as gr

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
prompt_template = """
As a security expert specializing in Threat Modeling for a fintech company, your task is to conduct a thorough threat analysis for the {service_name} service. Here are the specific details to consider:

### Service Details:
- **Description:** {description}
- **Interface Type:** {interface_type}
- **Technology Stack:** {technology_stack}
- **Use Cases:** {use_cases}

Given the financial nature of the company, it's crucial to scrutinize potential risks comprehensively. Your output should be in the form of a detailed table presenting the results of the threat modeling exercise. The table should encompass the following columns:

1. **Threat:** 
2. **Attack Path:** 
3. **Impact:** 
4. **Likelihood:** 
5. **Mitigation:**
6. **Notes:** 

And order by Impact * Likelihood descending.

Given the sensitive nature of financial services, ensure your analysis is meticulous and covers a spectrum of potential threats pertinent to the {service_name} service.
"""

llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

default_service_name = "ApplePay on Web Support"

default_description = """
Apple Pay represents an innovative mobile payment solution designed to streamline transactions across various Apple devices, offering unparalleled convenience, security, and privacy for users. Functioning seamlessly within iOS apps, watchOS apps, and Safari-enabled websites, Apple Pay effectively eliminates the need for physical cards or cash, introducing a more efficient payment method.

One of its key security features lies in the way it handles sensitive information. When a user adds their bank card to their Wallet via Apple Pay, the service ensures that the actual card number remains unrecorded both on the user's device and Apple servers. Instead, Apple Pay generates a distinct Device Account Number, encrypts it, and securely stores it within the Secure Element residing in the user's iPhone or Apple Watch. This unique process replaces the traditional storage of card numbers and enhances security measures significantly.

Moreover, Apple Pay enhances transaction security by dynamically creating unique security codes for validation purposes, thereby reducing the reliance on static security codes typically found on physical cards. This dynamic approach adds an extra layer of protection against potential breaches or fraudulent activities.

In the context of Zuora, integration with Apple Pay allows for the creation of an Apple Pay payment method specifically for web-based transactions. While the creation of this payment method isn't supported directly through the Zuora UI, following the prescribed method enables users to establish and utilize Apple Pay for processing payments within the UI thereafter.

It's important to note that Apple Pay operates under the regulations and terms outlined by the Apple Pay Platform Web Merchant Terms and Conditions. Leveraging this platform necessitates a vigilant monitoring of transactions to identify any potentially fraudulent behavior continually. Monitoring efforts typically involve keeping an eye on various factors, including chargeback rates that exceed a certain threshold, with consistent or excessive chargebacks potentially leading to removal from the Apple Pay program.

Therefore, to maintain compliance and continued participation in the Apple Pay program, it's crucial to promptly report any suspicious or potentially fraudulent activities to Zuora, allowing for appropriate action to be taken to mitigate risks and uphold the integrity of the payment ecosystem.
"""

default_use_cases = """

1. **Integrating with Zuora HPM JS SDK for Apple Pay:**
   As a customer, the goal is to seamlessly integrate with Zuora's Hosted Payment Method (HPM) JavaScript Software Development Kit (SDK) to facilitate the collection of payment details for Apple Pay from users/subscribers. This integration aims to streamline the payment process, allowing users to conveniently provide their payment information and make their initial payment hassle-free. The focus is on ensuring a smooth onboarding experience for new subscribers by leveraging the Zuora HPM JS SDK's capabilities.

2. **Utilizing Gateway-Returned Recurring Token for Subsequent Payments:**
   As a customer, the objective is to utilize the recurring token provided by the payment gateway for subsequent transactions. Once the initial payment using Apple Pay has been processed and authenticated, the intention is to leverage the tokenized payment information securely stored by the gateway. This approach aims to enable effortless, recurring payments without requiring users to re-enter their payment details for each transaction, enhancing convenience and encouraging ongoing subscription or purchase behavior.

3. **Enabling User Selection of Apple Pay and Integration of Apple Pay Button:**
   As a customer, the aspiration is to provide users with the option to select Apple Pay as their preferred payment method during the checkout process. This involves prominently displaying the Apple Pay button, as provided by Apple, within the payment interface. The goal is to create a user-friendly experience where customers can easily identify and choose Apple Pay as their desired payment option, enhancing user satisfaction and encouraging adoption of this secure and convenient payment method.
"""


def run_threat_modeling(
    service_name, description, use_cases, interface_type, technology_stack
):
    return llm_chain.run(
        service_name=service_name,
        description=description,
        use_cases=use_cases,
        interface_type=interface_type,
        technology_stack=technology_stack,
    )


def setup_gradio():
    with gr.Blocks() as demo:
        service_name = gr.Textbox(label="Service Name", value=default_service_name)
        interface_type = gr.Dropdown(
            label="Type", choices=["Web", "API", "Web+API"], value="API"
        )
        technology_stack = gr.Dropdown(
            label="Technology Stack",
            choices=[
                "Java",
                "Ruby",
                "NodeJS",
                "Python",
                "MySQL",
                "Postgres",
                "MongoDB",
                "S3",
                "Spring Boot",
                "Rails",
            ],
            multiselect=True,
            allow_custom_value=True,
            value=["Java", "MySQL"],
        )
        description = gr.Textbox(
            label="Description", lines=3, value=default_description
        )
        use_cases = gr.Textbox(label="Use Cases", lines=6, value=default_use_cases)
        attachments = gr.File(label="Attachments")
        btn = gr.Button("Run Threat Modeling")
        threat_modeling = gr.Markdown(label="Threat Modeling")
        btn.click(
            run_threat_modeling,
            inputs=[
                service_name,
                description,
                use_cases,
                interface_type,
                technology_stack,
            ],
            outputs=[threat_modeling],
        )

    gr.close_all()
    demo.launch()


if __name__ == "__main__":
    setup_gradio()
