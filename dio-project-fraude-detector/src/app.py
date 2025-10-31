import streamlit as st
from services.blob_service import upload_file_to_blob
from services.credit_card_service import analyze_credit_card_document


def configure_interface():
    st.title("Upload de Arquivos para Detecção de Fraudes - DESAFIO DIO - Fake Docs")
    uploaded_file = st.file_uploader(
        "Escolha um arquivo PDF ou imagem", type=["pdf", "png", "jpg", "jpeg"]
    )
    if uploaded_file is not None:
        fileName = uploaded_file.name

        # Mostrar a imagem carregada
        st.image(uploaded_file, caption="Arquivo enviado", use_column_width=True)

        # Enviar para o Azure Blob Storage
        blob_url = upload_file_to_blob(uploaded_file, fileName)

        if blob_url:
            st.success("Arquivo carregado com sucesso!")

            # Analisar o documento
            credit_card_info = analyze_credit_card_document(blob_url)

            # Mostrar resultados
            show_validation_result(credit_card_info)
        else:
            st.error(f"Erro ao enviar o arquivo {fileName}.")


def show_validation_result(credit_card_info):
    st.write("Resultado da validação:")

    # Verificar se alguma informação foi encontrada
    has_valid_info = any(
        [
            credit_card_info.get("card_name"),
            credit_card_info.get("bank_name"),
            credit_card_info.get("expiry_date"),
            credit_card_info.get("card_number"),
        ]
    )

    if has_valid_info:
        st.markdown(
            f"<h1 style='color: green;'>Cartão Válido</h1>", unsafe_allow_html=True
        )

        if credit_card_info.get("card_name"):
            st.write(f"Nome do Titular: {credit_card_info['card_name']}")

        if credit_card_info.get("bank_name"):
            st.write(f"Banco Emissor: {credit_card_info['bank_name']}")

        if credit_card_info.get("expiry_date"):
            st.write(f"Data de Validade: {credit_card_info['expiry_date']}")

        if credit_card_info.get("card_number"):
            # Mascarar o número do cartão por segurança
            masked_number = (
                "**** **** **** " + str(credit_card_info["card_number"])[-4:]
                if len(str(credit_card_info["card_number"])) >= 4
                else credit_card_info["card_number"]
            )
            st.write(f"Número do Cartão: {masked_number}")
    else:
        st.markdown(
            f"<h1 style='color: red;'>Cartão Inválido</h1>", unsafe_allow_html=True
        )
        st.write("Esse cartão não é válido.")


if __name__ == "__main__":
    configure_interface()
