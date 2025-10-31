from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.config import Config


def analyze_credit_card_document(card_url):
    try:
        client = DocumentIntelligenceClient(
            endpoint=Config.DOC_INTELLIGENCE_ENDPOINT,
            credential=AzureKeyCredential(Config.DOC_INTELLIGENCE_KEY),
        )

        # Criar o request para análise
        analyze_request = AnalyzeDocumentRequest(url_source=card_url)

        # Chamar a API
        card_info = client.begin_analyze_document(
            model_id="prebuilt-creditCard", body=analyze_request
        )

        result = card_info.result()

        # Verificar se há documentos no resultado
        if not result.documents:
            return {
                "card_name": None,
                "bank_name": None,
                "expiry_date": None,
                "card_number": None,
            }

        # Processar o primeiro documento encontrado
        document = result.documents[0]
        fields = document.fields if hasattr(document, "fields") else {}

        extracted_info = {
            "card_name": None,
            "bank_name": None,
            "expiry_date": None,
            "card_number": None,
        }

        # Extrair informações dos campos
        if fields:
            # Para nome do portador
            for field_name in ["CardholderName", "Cardholder", "Name", "HolderName"]:
                if field_name in fields and fields[field_name]:
                    field_obj = fields[field_name]
                    if hasattr(field_obj, "content"):
                        extracted_info["card_name"] = field_obj.content
                        break
                    elif hasattr(field_obj, "value"):
                        extracted_info["card_name"] = field_obj.value
                        break

            # Para banco emissor
            for field_name in ["Issuer", "Bank", "BankName", "IssuerBank"]:
                if field_name in fields and fields[field_name]:
                    field_obj = fields[field_name]
                    if hasattr(field_obj, "content"):
                        extracted_info["bank_name"] = field_obj.content
                        break
                    elif hasattr(field_obj, "value"):
                        extracted_info["bank_name"] = field_obj.value
                        break

            # Para data de expiração
            for field_name in ["ExpirationDate", "Expiry", "ValidThru", "ValidUntil"]:
                if field_name in fields and fields[field_name]:
                    field_obj = fields[field_name]
                    if hasattr(field_obj, "content"):
                        extracted_info["expiry_date"] = field_obj.content
                        break
                    elif hasattr(field_obj, "value"):
                        extracted_info["expiry_date"] = field_obj.value
                        break

            # Para número do cartão
            for field_name in ["CardNumber", "Number", "PAN", "AccountNumber"]:
                if field_name in fields and fields[field_name]:
                    field_obj = fields[field_name]
                    if hasattr(field_obj, "content"):
                        extracted_info["card_number"] = field_obj.content
                        break
                    elif hasattr(field_obj, "value"):
                        extracted_info["card_number"] = field_obj.value
                        break

        return extracted_info

    except Exception as e:
        print(f"Erro ao analisar o documento: {e}")
        return {
            "card_name": None,
            "bank_name": None,
            "expiry_date": None,
            "card_number": None,
        }
