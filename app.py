
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("문자 대량 전송 시뮬레이터")

uploaded_file = st.file_uploader("수신자 목록 업로드 (이름, 전화번호 포함)", type=["xlsx", "csv"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith("xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            df = pd.read_csv(uploaded_file)
        st.write("업로드된 목록", df)

        template = st.text_area("문자 템플릿 입력", "예: {이름}님, 오늘 교육은 오후 2시입니다.")

        if st.button("문자 전송 (가상)"):
            sent_messages = []
            for _, row in df.iterrows():
                name = str(row["이름"])
                phone = str(row["전화번호"])
                message = template.replace("{이름}", name)
                sent_messages.append({"이름": name, "전화번호": phone, "문자내용": message})

            result_df = pd.DataFrame(sent_messages)
            st.success("가상 문자 전송 완료!")
            st.dataframe(result_df)

            buffer = BytesIO()
            result_df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)

            st.download_button(
                label="결과 엑셀 다운로드",
                data=buffer,
                file_name="문자전송_시뮬레이션결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
