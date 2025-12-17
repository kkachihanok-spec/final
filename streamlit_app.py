import streamlit as st

st.title("🎵 한국어 노래 가사 분석 & 번역기")
st.write("가사를 입력하면 **전체 번역**과 **단어별 품사 분석**을 동시에 수행합니다.")

from konlpy.tag import Okt
import pandas as pd
from googletrans import Translator

# 페이지 설정
st.set_page_config(page_title="K-Pop 가사 분석기", layout="wide", page_icon="🎵")

# 형태소 분석기 및 번역기 초기화
okt = Okt()
translator = Translator()

# --- 사이드바: 설정 ---
st.sidebar.header("설정")
target_language = st.sidebar.selectbox("번역할 언어 선택", ["English", "Japanese", "Chinese (Simplified)"], index=0)
lang_code = {'English': 'en', 'Japanese': 'ja', 'Chinese (Simplified)': 'zh-cn'}

# --- 메인 영역 ---
lyrics_input = st.text_area("노래 가사를 입력하세요:", height=250, placeholder="여기에 한국어 가사를 붙여넣으세요...")

if st.button("분석 및 번역 시작"):
    if lyrics_input.strip():
        # 레이아웃 나누기 (왼쪽: 번역, 오른쪽: 단어 분석)
        col1, col2 = st.columns(2)

        # 1. 가사 번역 (Google Translate)
        with col1:
            st.subheader("🌍 가사 번역")
            try:
                translation = translator.translate(lyrics_input, dest=lang_code[target_language])
                st.info(translation.text)
            except Exception as e:
                st.error("번역 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

        # 2. 단어 분석 (Konlpy)
        with col2:
            st.subheader("📊 주요 단어 분석")
            
            # 형태소 분석 (기본형 추출)
            morphs = okt.pos(lyrics_input, stem=True)
            
            unique_words = []
            seen = set()
            target_pos = ['Noun', 'Verb', 'Adjective', 'Adverb']
            
            for word, pos in morphs:
                # 2글자 이상이며 특정 품사만 필터링
                if pos in target_pos and len(word) > 1 and word not in seen:
                    unique_words.append({'단어': word, '품사': pos})
                    seen.add(word)
            
            if unique_words:
                df = pd.DataFrame(unique_words)
                
                # 품사 한글화
                pos_map = {'Noun': '명사', 'Verb': '동사', 'Adjective': '형용사', 'Adverb': '부사'}
                df['품사'] = df['품사'].map(pos_map)
                
                # 사전 링크 생성
                df['사전 링크'] = df['단어'].apply(lambda x: f"https://ko.dict.naver.com/#/search?query={x}")
                
                # 테이블 표시
                st.dataframe(df, use_container_width=True)
            else:
                st.write("분석할 명사, 동사, 형용사가 없습니다.")

        st.divider()
        st.success("✅ 분석이 완료되었습니다!")
        
    else:
        st.warning("분석할 가사를 입력해 주세요.")

# 하단 안내
st.caption("Powered by Konlpy (Okt) & Google Translate")
